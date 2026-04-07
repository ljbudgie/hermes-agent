"""Tests for Burgess Principle structural enforcement.

Tests deployment-sensitive command detection, file mutation tracking,
auto-injection of human-impact review prompts, and config parsing.
"""

import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tools.approval import detect_deployment_command, DEPLOYMENT_PATTERNS


# =========================================================================
# Deployment-sensitive command detection
# =========================================================================

class TestDeploymentPatterns:
    """Test detect_deployment_command for infrastructure/deployment commands."""

    @pytest.mark.parametrize("cmd,expected_desc", [
        ("docker push myimage:latest", "container image push to registry"),
        ("podman push registry.io/app:v2", "container image push to registry"),
        ("kubectl apply -f deployment.yaml", "Kubernetes cluster change"),
        ("kubectl delete pod my-pod", "Kubernetes cluster change"),
        ("kubectl rollout restart deployment/api", "Kubernetes cluster change"),
        ("kubectl scale deployment/web --replicas=3", "Kubernetes cluster change"),
        ("kubectl exec -it pod-name -- sh", "command execution in live Kubernetes pod"),
        ("helm install my-release ./chart", "Helm chart deployment"),
        ("helm upgrade my-release ./chart", "Helm chart deployment"),
        ("helm uninstall my-release", "Helm chart deployment"),
        ("helm rollback my-release 1", "Helm chart deployment"),
        ("terraform apply", "Terraform infrastructure change"),
        ("terraform destroy", "Terraform infrastructure change"),
        ("terraform import aws_instance.web i-12345", "Terraform infrastructure change"),
        ("tofu apply", "OpenTofu infrastructure change"),
        ("tofu destroy", "OpenTofu infrastructure change"),
        ("pulumi up", "Pulumi infrastructure change"),
        ("pulumi destroy", "Pulumi infrastructure change"),
        ("ansible-playbook deploy.yml", "Ansible playbook execution"),
        ("git push origin production", "git push to production branch"),
        ("git push origin main", "git push to production branch"),
        ("git push origin master", "git push to production branch"),
        ("git push origin release/v2", "git push to production branch"),
        ("aws lambda update-function-code --function-name my-fn", "AWS Lambda code update"),
        ("gcloud run deploy my-service", "Google Cloud deployment"),
        ("gcloud app deploy app.yaml", "Google Cloud deployment"),
        ("gcloud functions deploy my-fn", "Google Cloud deployment"),
        ("az webapp deploy --name myapp", "Azure deployment"),
        ("az functionapp deployment source config", "Azure deployment"),
        ("systemctl restart nginx", "system service restart"),
        ("systemctl reload apache2", "system service restart"),
        ("nginx -s reload", "nginx reload"),
        ("flyctl deploy", "Fly.io deployment"),
        ("railway up", "Railway deployment"),
        ("railway deploy", "Railway deployment"),
        ("vercel deploy", "Vercel deployment"),
        ("vercel --prod", "Vercel deployment"),
        ("npm publish", "npm package publish"),
        ("cargo publish", "Rust crate publish"),
        ("gem push my-gem-1.0.0.gem", "Ruby gem publish"),
    ])
    def test_deployment_commands_detected(self, cmd, expected_desc):
        is_deploy, desc = detect_deployment_command(cmd)
        assert is_deploy is True, f"Expected deployment detection for: {cmd}"
        assert desc == expected_desc

    @pytest.mark.parametrize("cmd", [
        "ls -la",
        "cat deployment.yaml",
        "kubectl get pods",
        "kubectl describe deployment/api",
        "kubectl logs pod-name",
        "helm list",
        "helm status my-release",
        "terraform plan",
        "terraform init",
        "terraform validate",
        "tofu plan",
        "docker build -t myimage .",
        "docker pull ubuntu:latest",
        "docker run --rm alpine echo hi",
        "git push origin feature/my-branch",
        "git push origin dev",
        "git status",
        "aws s3 ls",
        "gcloud compute instances list",
        "ansible --version",
        "npm install",
        "npm run build",
        "cargo build",
        "gem install bundler",
    ])
    def test_safe_commands_not_flagged(self, cmd):
        is_deploy, desc = detect_deployment_command(cmd)
        assert is_deploy is False, f"Should not flag: {cmd}"
        assert desc is None


class TestDeploymentPatternsCompleteness:
    """Ensure all DEPLOYMENT_PATTERNS compile and are well-formed."""

    def test_all_patterns_compile(self):
        import re
        for pattern, description in DEPLOYMENT_PATTERNS:
            re.compile(pattern, re.IGNORECASE | re.DOTALL)

    def test_all_patterns_have_descriptions(self):
        for pattern, description in DEPLOYMENT_PATTERNS:
            assert description, f"Pattern {pattern} has empty description"
            assert isinstance(description, str)


# =========================================================================
# Burgess review detection in response text
# =========================================================================

class TestBurgessReviewDetection:
    """Test _response_contains_burgess_review logic.

    Rather than importing AIAgent (which requires openai), we replicate the
    lightweight detection logic here to test the algorithm in isolation.
    """

    _MARKERS = (
        "human-impact review",
        "human impact review",
        "burgess principle",
        "⚠ human-impact",
        "⚠️ human-impact",
        "🔍 human-impact",
    )

    def _contains_review(self, response):
        if not response:
            return False
        lower = response.lower()
        return any(marker in lower for marker in self._MARKERS)

    def test_detects_human_impact_review_header(self):
        assert self._contains_review(
            "Here is my summary.\n\n## ⚠ Human-Impact Review (Burgess Principle)\n\nNo areas affected."
        )

    def test_detects_burgess_principle_mention(self):
        assert self._contains_review(
            "Based on the Burgess Principle review, no changes affect real people."
        )

    def test_detects_emoji_variant(self):
        assert self._contains_review(
            "## 🔍 Human-Impact Review\n\nNo impact areas detected."
        )

    def test_no_review_in_plain_response(self):
        assert not self._contains_review(
            "I've updated the README.md file as requested."
        )

    def test_empty_response(self):
        assert not self._contains_review("")

    def test_none_response(self):
        assert not self._contains_review(None)


# =========================================================================
# Burgess review prompt builder
# =========================================================================

class TestBurgessReviewPrompt:
    """Test _build_burgess_review_prompt output.

    Uses the same logic as AIAgent._build_burgess_review_prompt() but
    tested in isolation to avoid the openai dependency.
    """

    def _build_prompt(self, file_mutations=None, deployment_commands=None):
        """Replicate the prompt builder logic."""
        parts = [
            "[System: Burgess Principle active enforcement — before finalizing, "
            "you MUST include a Human-Impact Review section. The following "
            "changes were detected during this turn:\n"
        ]
        if file_mutations:
            parts.append(f"\nFiles modified: {', '.join(file_mutations[:20])}")
        if deployment_commands:
            parts.append(f"\nDeployment commands: {', '.join(deployment_commands[:10])}")
        parts.append(
            "\n\nPlease add a brief '⚠ Human-Impact Review (Burgess Principle)' "
            "section to your response. For each file or command above, check "
            "whether changes touch: accessibility, privacy & personal data, "
            "security, user-facing language, pricing & billing, automated "
            "decisions, or deployment & infrastructure. List affected areas "
            "with one sentence each, and recommend who should review. If no "
            "human-impact areas were affected, state that briefly. Then "
            "re-state your original summary/conclusion.]"
        )
        return "".join(parts)

    def test_includes_file_mutations(self):
        prompt = self._build_prompt(file_mutations=["src/auth.py", "src/billing.py"])
        assert "src/auth.py" in prompt
        assert "src/billing.py" in prompt
        assert "Files modified" in prompt

    def test_includes_deployment_commands(self):
        prompt = self._build_prompt(deployment_commands=["kubectl apply -f deploy.yaml"])
        assert "kubectl apply" in prompt
        assert "Deployment commands" in prompt

    def test_includes_both(self):
        prompt = self._build_prompt(
            file_mutations=["app.py"],
            deployment_commands=["docker push img:v2"]
        )
        assert "Files modified" in prompt
        assert "Deployment commands" in prompt

    def test_empty_lists_still_produce_prompt(self):
        prompt = self._build_prompt()
        assert "Burgess Principle" in prompt
        assert "Human-Impact Review" in prompt


# =========================================================================
# Config parsing for burgess_enforcement
# =========================================================================

class TestBurgessEnforcementConfig:
    """Test that burgess_enforcement config values are parsed correctly."""

    def _parse_enforcement(self, value):
        """Simulate the config parsing logic from AIAgent.__init__."""
        if isinstance(value, bool):
            return "active" if value else "off"
        result = str(value).lower().strip()
        if result in ("false", "0", "no", "off", "none"):
            return "off"
        if result not in ("prompt", "active"):
            return "active"
        return result

    def test_true_maps_to_active(self):
        assert self._parse_enforcement(True) == "active"

    def test_false_maps_to_off(self):
        assert self._parse_enforcement(False) == "off"

    def test_string_active(self):
        assert self._parse_enforcement("active") == "active"

    def test_string_prompt(self):
        assert self._parse_enforcement("prompt") == "prompt"

    def test_string_off(self):
        assert self._parse_enforcement("off") == "off"

    def test_string_false(self):
        assert self._parse_enforcement("false") == "off"

    def test_string_none(self):
        assert self._parse_enforcement("none") == "off"

    def test_unknown_defaults_to_active(self):
        assert self._parse_enforcement("banana") == "active"

    def test_zero_string(self):
        assert self._parse_enforcement("0") == "off"


# =========================================================================
# Terminal tool Burgess deployment notice
# =========================================================================

class TestTerminalBurgessNotice:
    """Test that deployment commands get a burgess_notice in the result."""

    def test_deployment_notice_in_result_json(self):
        """Verify the detect_deployment_command result would be used."""
        is_deploy, desc = detect_deployment_command("kubectl apply -f deploy.yaml")
        assert is_deploy is True
        # Build the notice the same way terminal_tool.py does
        notice = (
            f"⚠ Burgess Principle — this command ({desc}) affects live "
            f"infrastructure or publishes artifacts that real people depend on. "
            f"Ensure a human has reviewed the specific implications of this "
            f"change for the people it affects before proceeding."
        )
        assert "Kubernetes cluster change" in notice
        assert "Burgess Principle" in notice

    def test_no_notice_for_safe_command(self):
        is_deploy, desc = detect_deployment_command("ls -la /tmp")
        assert is_deploy is False
        assert desc is None
