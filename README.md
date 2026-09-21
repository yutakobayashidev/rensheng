# Rensheng

Renshengは、privateな生活コンテキストを本人の手元に保存し、人間とAIがあとから辿れる小さなMarkdownへ継続的にコンパイルするlocal-firstな基盤です。

## Personal repository template

[`template/`](template/) は、個人用Renshengリポジトリの匿名スターターです。実データは含まず、次のものだけを提供します。

- `philosophy.md` — Renshengの境界と設計原則
- `profile/`、`goals.md`、`recent-updates.md` — Personal Contextの最小構成
- `people/`、`health/`、`money/`など — 空のDomain構造
- `.agents/skills/` — Renshengを読むAgent向けの汎用Skill

新しいprivateリポジトリへ展開します。

```console
mkdir -p /path/to/private-rensheng
cp -a template/. /path/to/private-rensheng/
```

生成先はprivateにし、プロフィール、健康、金銭、対人関係などの個人データをこのpublicリポジトリへコミットしないでください。

## Components

- [OpenBrief](docs/openbrief.md)
