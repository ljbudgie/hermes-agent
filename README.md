<p align="center">
  <img src="assets/banner.png" alt="Hermes Agent" width="100%">
</p>

# Hermes Agent ☤

<p align="center">
  <a href="https://hermes-agent.nousresearch.com/docs/"><img src="https://img.shields.io/badge/Docs-hermes--agent.nousresearch.com-FFD700?style=for-the-badge" alt="Documentation"></a>
  <a href="https://discord.gg/NousResearch"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://github.com/NousResearch/hermes-agent/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://nousresearch.com"><img src="https://img.shields.io/badge/Built%20by-Nous%20Research-blueviolet?style=for-the-badge" alt="Built by Nous Research"></a>
</p>

**The self-improving AI agent built by [Nous Research](https://nousresearch.com).** It's the only agent with a built-in learning loop — it creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions. Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop — talk to it from Telegram while it works on a cloud VM.

Use any model you want — 18 providers out of the box including [Nous Portal](https://portal.nousresearch.com) (400+ models), [OpenRouter](https://openrouter.ai), Anthropic, OpenAI, Google Gemini, DeepSeek, [Hugging Face](https://huggingface.co), [z.ai/GLM](https://z.ai), [Kimi](https://platform.moonshot.ai), [MiniMax](https://www.minimax.io), Alibaba DashScope, and more. Configure multiple API keys per provider with automatic rotation, or set up ordered fallback chains across providers. Switch with `hermes model` — no code changes, no lock-in.

<table>
<tr><td><b>A real terminal interface</b></td><td>Full TUI with multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, streaming tool output, inline diff previews, and <a href="#skinnable-themes">customizable themes</a>.</td></tr>
<tr><td><b>Lives where you do</b></td><td><a href="#platform-support">15 messaging platforms</a> — Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Feishu/Lark, WeCom, DingTalk, Mattermost, Email, SMS, Home Assistant, webhooks, and an OpenAI-compatible API server. Voice memo transcription, cross-platform conversation continuity.</td></tr>
<tr><td><b>Profiles</b></td><td><a href="#profiles--multi-instance">Fully isolated agent instances</a> — each with its own config, memory, sessions, skills, and gateway. Run a coding assistant, a research agent, and a devops bot side-by-side without interference.</td></tr>
<tr><td><b>Pluggable memory</b></td><td>A closed learning loop with a <a href="#pluggable-memory-system">pluggable provider interface</a>. Built-in memory (MEMORY.md, USER.md, FTS5 session search) is always on. Add <a href="https://github.com/plastic-labs/honcho">Honcho</a>, Mem0, Holographic, or any third-party backend as a plugin — one active at a time, alongside the built-in layer. Compatible with the <a href="https://agentskills.io">agentskills.io</a> skill standard.</td></tr>
<tr><td><b>MCP — both ways</b></td><td>Connect any MCP server to extend the agent's tools. Or run <code>hermes mcp serve</code> to <a href="#mcp-server-mode">expose Hermes as an MCP server</a> for Claude Desktop, Cursor, VS Code, and other MCP clients. Editor integrations (ACP) can also register their own MCP servers as agent tools.</td></tr>
<tr><td><b>Scheduled automations</b></td><td>Built-in cron scheduler with delivery to any of the 15 platforms. Daily reports, nightly backups, weekly audits — all in natural language, running unattended.</td></tr>
<tr><td><b>Delegates and parallelizes</b></td><td>Spawn isolated subagents for parallel workstreams. Write Python scripts that call tools via RPC, collapsing multi-step pipelines into zero-context-cost turns.</td></tr>
<tr><td><b>Runs anywhere, not just your laptop</b></td><td>Seven terminal backends — local, <a href="#docker">Docker</a>, SSH, Daytona, Singularity, Modal, and Managed Modal. Daytona and Modal offer serverless persistence — your agent's environment hibernates when idle and wakes on demand.</td></tr>
<tr><td><b>Security in depth</b></td><td>Pattern-based <a href="#security">command approval</a> with smart auxiliary-model review. Secret exfiltration blocking — scans tool outputs, browser URLs, and LLM responses for leaked credentials. Container isolation. DM pairing. Credential directory protection.</td></tr>
<tr><td><b>Human-impact awareness</b></td><td>Built-in <a href="#the-burgess-principle--human-impact-awareness">Burgess Principle</a> integration — enabled by default. The agent flags changes that affect real people (accessibility, privacy, billing, automated decisions) and recommends human review before shipping. Five advocacy skills for contract review, data access requests, and more.</td></tr>
<tr><td><b>Research-ready</b></td><td>Batch trajectory generation, Atropos RL environments, trajectory compression for training the next generation of tool-calling models.</td></tr>
</table>

---

## Quick Install

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Works on Linux, macOS, and WSL2. The installer handles everything — Python, Node.js, dependencies, and the `hermes` command. No prerequisites except git.

> **Windows:** Native Windows is not supported. Please install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and run the command above.

After installation:

```bash
source ~/.bashrc    # reload shell (or: source ~/.zshrc)
hermes              # start chatting!
```

### Docker

An official Dockerfile is included for containerized deployments:

```bash
docker build -t hermes-agent .
docker run -it -v ~/.hermes:/opt/data hermes-agent          # CLI mode
docker run -d  -v ~/.hermes:/opt/data hermes-agent gateway  # Gateway mode
```

The container includes Python, Node.js, ripgrep, FFmpeg, and Playwright — everything the agent needs.

---

## Getting Started

```bash
hermes              # Interactive CLI — start a conversation
hermes model        # Choose your LLM provider and model
hermes tools        # Configure which tools are enabled
hermes skills       # Browse and manage skills
hermes config set   # Set individual config values
hermes gateway      # Start the messaging gateway
hermes setup        # Run the full setup wizard (configures everything at once)
hermes -p work ...  # Run any command under a named profile
hermes doctor       # Diagnose any issues
hermes update       # Update to the latest version
```

📖 **[Full documentation →](https://hermes-agent.nousresearch.com/docs/)**

---

## Platform Support

Hermes runs as a CLI and connects to 15 messaging platforms through a single gateway process. Set up any combination with `hermes gateway setup`.

| Platform | Highlights |
|----------|-----------|
| **Telegram** | Polling and webhook modes. Group/supergroup support with mention gating (always, mention-only, regex). Media groups, voice memos, topics. |
| **Discord** | Voice channels with Opus codec. Thread support. Slash commands. |
| **Slack** | Multi-workspace via comma-separated tokens. Socket Mode. `/hermes` slash commands. File/image/audio attachments. |
| **WhatsApp** | Business API, whatsapp-web.js, or Baileys backends. Media attachments and status updates. |
| **Signal** | End-to-end encrypted messaging via signal-cli. |
| **Matrix** | Room/space support. Thread support. Optional end-to-end encryption via matrix-nio. |
| **Feishu / Lark** | Enterprise messaging with event subscriptions, message cards, rich formatting, and group chat. |
| **WeCom** | Enterprise WeChat — text, image, and voice messages. Group chats with callback verification. |
| **DingTalk** | Alibaba enterprise messaging via Stream Mode. |
| **Mattermost** | Self-hosted Slack alternative. REST API and WebSocket. |
| **Email** | IMAP/SMTP with multi-account support. |
| **SMS** | Twilio integration for text messaging. |
| **Home Assistant** | Smart home automation control via WebSocket. |
| **Webhook** | Generic HTTP ingress/egress — connect GitHub, GitLab, JIRA, or any webhook source. |
| **API Server** | OpenAI-compatible REST API with session continuity (`X-Hermes-Session-Id`), real-time tool progress streaming via SSE, and chat completions endpoint. |

---

## LLM Providers

Eighteen providers are supported out of the box. Switch at any time with `hermes model` or the `/model` slash command.

| Provider | Notes |
|----------|-------|
| [Nous Portal](https://portal.nousresearch.com) | 400+ models through a single endpoint |
| [OpenRouter](https://openrouter.ai) | 200+ models, automatic routing |
| [Anthropic](https://anthropic.com) | Claude family with prompt caching |
| [OpenAI](https://openai.com) | GPT family |
| [OpenAI Codex](https://openai.com) | Codex models via OAuth device flow |
| [Google Gemini](https://ai.google.dev) | Gemini family via AI Studio |
| [DeepSeek](https://deepseek.com) | DeepSeek models |
| [Hugging Face](https://huggingface.co) | Inference API with live endpoint probing |
| [z.ai / GLM](https://z.ai) | GLM models |
| [Kimi / Moonshot](https://platform.moonshot.ai) | Kimi and Moonshot models |
| [MiniMax](https://www.minimax.io) | MiniMax models (global and China endpoints) |
| [Alibaba DashScope](https://dashscope.aliyun.com) | Qwen family |
| [GitHub Copilot](https://github.com/features/copilot) | Via API key or ACP adapter |
| OpenCode Zen / Go | Community model endpoints |
| AI Gateway | Custom gateway routing |
| Kilo Code | Community provider |
| Any OpenAI-compatible endpoint | Point `base_url` at your own server |

### Credential pools

Configure multiple API keys per provider for automatic rotation:

```yaml
# In ~/.hermes/config.yaml
credential_pool_strategies:
  anthropic: least_used    # round_robin, random, fill_first also available
```

Keys are rotated automatically. If a key returns a 401 or rate-limit error, the pool fails over to the next credential.

### Fallback provider chains

Set up ordered failover across providers so your agent keeps working even if a provider goes down:

```yaml
fallback_providers:
  - anthropic
  - openrouter
  - nous
```

---

## Profiles — Multi-Instance

Run multiple fully isolated Hermes instances, each with its own config, API keys, memory, sessions, skills, and gateway service.

```bash
hermes profile create work                # New empty profile
hermes profile create work --clone        # Clone config and API keys from default
hermes profile create work --clone-all    # Full copy of current profile

hermes -p work                            # Start CLI with the "work" profile
hermes -p work gateway start              # Start gateway under "work" profile
hermes profile use work                   # Set "work" as the sticky default

hermes profile list                       # Show all profiles
hermes profile delete old-project         # Remove a profile
```

Each profile lives in `~/.hermes/profiles/<name>/` with its own `config.yaml`, `.env`, `SOUL.md`, memories, sessions, skills, skins, and cron jobs. The default profile remains at `~/.hermes/`.

---

## Pluggable Memory System

Hermes has a two-layer memory architecture:

1. **Built-in memory** (always on) — MEMORY.md for facts, USER.md for user modeling, FTS5-indexed session search with LLM summarization for cross-session recall.

2. **External memory provider** (optional, one at a time) — a pluggable interface that any third-party backend can implement. Providers ship as plugins in `plugins/memory/<name>/` with a `plugin.yaml` manifest.

Available memory providers:

| Provider | Description |
|----------|-------------|
| **Built-in** | File-based memory + SQLite FTS5 session search (always active) |
| [Honcho](https://github.com/plastic-labs/honcho) | Dialectic user modeling with session tagging |
| Mem0 | Personal AI memory layer |
| Holographic | Vector-based semantic memory with retrieval |
| Hindsight | Structured memory with reflections |
| RetainDB | Persistent structured recall |
| ByteRover | Memory with analytics |
| OpenViking | Long-term conversational memory |

Set your provider in `config.yaml`:

```yaml
memory:
  provider: honcho    # or: mem0, holographic, hindsight, retaindb, byterover, openviking
```

Building your own provider? Subclass `MemoryProvider` from `agent/memory_provider.py` and implement the required methods (`is_available`, `initialize`, `prefetch`, `sync_turn`, etc.).

---

## MCP Server Mode

Hermes can act as an MCP server, exposing its conversations and capabilities to other AI tools:

```bash
hermes mcp serve              # Start the MCP server
hermes mcp serve --verbose    # With debug logging
```

This lets Claude Desktop, Cursor, VS Code, Zed, and any MCP-compatible client browse Hermes conversations, search sessions, and interact with the agent. The ACP adapter also allows editors to register their own MCP servers as additional agent tools.

---

## Security

### Command approval

Every potentially dangerous command goes through a pattern-based approval gate before execution. Hermes detects 20+ dangerous patterns — recursive deletes, world-writable permissions, disk formatting, SQL drops without WHERE clauses, credential file writes, and more.

The approval flow: the agent proposes a command → pattern matching flags it → you approve or reject. Approved patterns can be added to a permanent allowlist. A smart auxiliary model can auto-approve low-risk commands when configured.

### Secret exfiltration blocking

Hermes actively prevents credential leakage:

- Scans browser URLs and LLM responses for secret patterns (API keys, tokens, credentials)
- Redacts sensitive values from `execute_code` sandbox output
- Protects credential directories (`.docker`, `.azure`, `.config/gh`, and more)
- Blocks URL-encoding and base64-encoding evasion attempts

### Container isolation

Run the agent's terminal in Docker, Singularity, or Modal containers to sandbox all command execution away from your host system.

---

## The Burgess Principle — Human-Impact Awareness

Hermes is the first AI agent with built-in [Burgess Principle](https://github.com/ljbudgie/burgess-principle) support — **enabled by default**. The core question it applies:

> *"Was a human member of the team able to personally review the specific implications of this change for the people it affects?"*

Hermes automatically flags changes that touch accessibility, privacy, personal data, security, user-facing language, pricing, automated decisions, or deployment — and recommends who should review them before shipping.

### How it helps the AI agent

The Burgess Principle gives Hermes something most AI agents lack: a structured self-check for whether its work might affect real people in ways that deserve human attention. Without it, an AI agent can confidently ship code that changes billing logic, tightens access controls, or modifies error messages without ever pausing to consider the people on the receiving end.

With the principle built into its system prompt, Hermes automatically scans its own changes against seven human-impact areas (accessibility, privacy, security, user-facing language, pricing, automated decisions, and deployment). When it detects impact, it flags it clearly and recommends *who* should review — not just "someone", but a specific role like "a designer should check the new error flow" or "a security engineer should review the auth changes." This makes the agent a more responsible collaborator: it still moves fast, but it knows when to slow down and ask a human to look.

The principle also helps the agent assist *you* directly. Drop the [Burgess Principle repository](https://github.com/ljbudgie/burgess-principle) into a conversation (or install the advocacy skills) and Hermes can draft polite, firm letters asking institutions whether a real person reviewed your specific situation — for council tax disputes, automated credit decisions, accessibility requests, data access rights, and more. The same calm question works in any country, against any institution.

Use the `/review` slash command in any session to run an on-demand human-impact review of changes made so far.

### Advocacy skills

Five optional skills in `optional-skills/advocacy/` extend the Burgess Principle beyond code review:

| Skill | What it does |
|-------|-------------|
| `coding-agent-review` | Scans code changes for human-impact areas before finalizing |
| `contract-review` | Reviews contracts and terms of service for clauses that bypass individual human review |
| `human-review-request` | Drafts polite, firm letters to institutions asking whether a human reviewed your case |
| `dsar-request` | Drafts Data Subject Access Requests with the Burgess question built in |
| `reasonable-adjustments` | Helps request accessibility adjustments with the right legal framework |

Install any of them:

```bash
hermes skills browse --source official   # find them under "advocacy"
hermes skills install coding-agent-review
```

*The Burgess Principle is a UK Certification Mark (UK00004343685) by Lewis James Burgess, free for personal use under MIT licence.*

---

## Skinnable Themes

Customize the CLI's look and feel with the data-driven skin engine — no code changes needed.

```bash
/skin list              # Show available skins
/skin ares              # Switch to a different theme
```

Built-in skins: **default** (gold/kawaii), **ares** (crimson war-god), **mono** (grayscale), **slate** (cool blue). Or create your own in `~/.hermes/skins/<name>.yaml`:

```yaml
name: cyberpunk
description: Neon-soaked terminal theme
colors:
  banner_border: "#FF00FF"
  banner_title: "#00FFFF"
  response_border: "#FF1493"
spinner:
  thinking_verbs: ["jacking in", "decrypting", "uploading"]
branding:
  agent_name: "Cyber Agent"
```

Skins customize banner colors, spinner animations, tool output prefixes, per-tool emojis, branding text, and the response box style.

---

## CLI vs Messaging Quick Reference

Hermes has two entry points: start the terminal UI with `hermes`, or run the gateway and talk to it from any of the 15 supported platforms. Once you're in a conversation, many slash commands are shared across both interfaces.

| Action | CLI | Messaging platforms |
|---------|-----|---------------------|
| Start chatting | `hermes` | Run `hermes gateway setup` + `hermes gateway start`, then send the bot a message |
| Start fresh conversation | `/new` or `/reset` | `/new` or `/reset` |
| Change model | `/model [provider:model]` | `/model [provider:model]` |
| Set a personality | `/personality [name]` | `/personality [name]` |
| Retry or undo the last turn | `/retry`, `/undo` | `/retry`, `/undo` |
| Compress context / check usage | `/compress`, `/usage`, `/insights [--days N]` | `/compress`, `/usage`, `/insights [days]` |
| Browse skills | `/skills` or `/<skill-name>` | `/skills` or `/<skill-name>` |
| Run human-impact review | `/review` | `/review` |
| Switch skin/theme | `/skin [name]` | — |
| Interrupt current work | `Ctrl+C` or send a new message | `/stop` or send a new message |
| Platform-specific status | `/platforms` | `/status`, `/sethome` |

For the full command lists, see the [CLI guide](https://hermes-agent.nousresearch.com/docs/user-guide/cli) and the [Messaging Gateway guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging).

---

## Skills System

Skills are procedural memory — reusable instructions the agent creates from experience or installs from external sources. Over 60 official skills ship in `optional-skills/` across 15 categories:

| Category | Examples |
|----------|---------|
| **Advocacy** | Coding agent review, contract review, DSAR requests, reasonable adjustments |
| **MLOps** | PyTorch Lightning, Hugging Face tokenizers, Flash Attention, TensorRT, FAISS, Chroma, Qdrant |
| **Research** | Bioinformatics, domain intel, DuckDuckGo search, parallel CLI, GitNexus explorer |
| **Security** | 1Password integration, OSS forensics, Sherlock OSINT |
| **DevOps** | Docker management, CLI tooling |
| **Creative** | Blender MCP, meme generation |
| **Productivity** | Canvas, flashcards, Siyuan notes, telephony |
| **Blockchain** | Solana, Base |
| **Autonomous AI** | Blackbox, Honcho |

Browse and install from multiple sources:

```bash
hermes skills search "pytorch"            # Search all sources
hermes skills install coding-agent-review  # Install a skill
hermes skills list                         # List installed skills
/skills                                    # Browse from within a conversation
```

Skill sources include the official bundle, GitHub repositories, ClawhubSource (cloud registry), Claude Marketplace, and LobeHub community skills. All community skills are scanned before activation.

---

## Documentation

All documentation lives at **[hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs/)**:

| Section | What's Covered |
|---------|---------------|
| [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart) | Install → setup → first conversation in 2 minutes |
| [CLI Usage](https://hermes-agent.nousresearch.com/docs/user-guide/cli) | Commands, keybindings, personalities, sessions, skins |
| [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) | Config file, providers, credential pools, fallback chains, all options |
| [Messaging Gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging) | All 15 platforms — setup, webhook modes, group controls, multi-workspace |
| [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security) | Command approval, secret exfiltration blocking, DM pairing, container isolation |
| [Tools & Toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools) | 40+ tools, toolset system, terminal backends, Camofox browser |
| [Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) | Procedural memory, Skills Hub, creating and installing skills |
| [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) | Pluggable memory providers, built-in memory, user profiles |
| [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/features/profiles) | Multi-instance support, profile creation, isolation |
| [MCP Integration](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) | Connect MCP servers, run Hermes as an MCP server, ACP editor integration |
| [Cron Scheduling](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) | Scheduled tasks with delivery to any platform |
| [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files) | SOUL.md, AGENTS.md, .cursorrules — project context that shapes every conversation |
| [Burgess Principle](https://github.com/ljbudgie/burgess-principle) | Human-impact review, advocacy skills, `/review` command |
| [Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture) | Project structure, agent loop, key classes |
| [Contributing](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing) | Development setup, PR process, code style |
| [CLI Reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) | All commands and flags |
| [Environment Variables](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) | Complete env var reference |

---

## Migrating from OpenClaw

If you're coming from OpenClaw, Hermes can automatically import your settings, memories, skills, and API keys.

**During first-time setup:** The setup wizard (`hermes setup`) automatically detects `~/.openclaw` and offers to migrate before configuration begins.

**Anytime after install:**

```bash
hermes claw migrate              # Interactive migration (full preset)
hermes claw migrate --dry-run    # Preview what would be migrated
hermes claw migrate --preset user-data   # Migrate without secrets
hermes claw migrate --overwrite  # Overwrite existing conflicts
```

What gets imported:
- **SOUL.md** — persona file
- **Memories** — MEMORY.md and USER.md entries
- **Skills** — user-created skills → `~/.hermes/skills/openclaw-imports/`
- **Command allowlist** — approval patterns
- **Messaging settings** — platform configs, allowed users, working directory
- **API keys** — allowlisted secrets (Telegram, OpenRouter, OpenAI, Anthropic, ElevenLabs)
- **TTS assets** — workspace audio files
- **Workspace instructions** — AGENTS.md (with `--workspace-target`)

See `hermes claw migrate --help` for all options, or use the `openclaw-migration` skill for an interactive agent-guided migration with dry-run previews.

---

## Contributing

We welcome contributions! See the [Contributing Guide](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing) for development setup, code style, and PR process.

Quick start for contributors:

```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all,dev]"
python -m pytest tests/ -q
```

> **RL Training (optional):** To work on the RL/Tinker-Atropos integration:
> ```bash
> git submodule update --init tinker-atropos
> uv pip install -e "./tinker-atropos"
> ```

---

## Community

- 💬 [Discord](https://discord.gg/NousResearch)
- 📚 [Skills Hub](https://agentskills.io)
- 🐛 [Issues](https://github.com/NousResearch/hermes-agent/issues)
- 💡 [Discussions](https://github.com/NousResearch/hermes-agent/discussions)

---

## License

MIT — see [LICENSE](LICENSE).

Built by [Nous Research](https://nousresearch.com).
