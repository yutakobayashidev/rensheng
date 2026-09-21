# Rensheng in Context

Rensheng specifies how private life context should be preserved, compiled, and read across tools and Agents. Its distinctive emphasis is the combination of personal continuity, explicit information boundaries, source-backed current state, and the user's authority over their own goals and identity. See the [design philosophy](template/philosophy.md) and [Agent guidelines](template/AGENTS.md).

Source review: **2026-09-21 (UTC)**. Rensheng baseline: [77f84a3](https://github.com/yutakobayashidev/rensheng/tree/77f84a38a3572246977a261b7dad6d3fce9ca82d).

The tables compare published designs and documented capabilities. Rensheng's intended behavior is distinguished from its current implementation below. Relationships and architectural positioning are this document's interpretation of the linked sources; they are not benchmark results or claims of historical priority.

## Positioning at a glance

| System | Kind | Main unit | Main emphasis | Relationship to Rensheng |
| --- | --- | --- | --- | --- |
| **Rensheng** | Project, repository template, and operating conventions | Source-linked Personal Context | Resume life with less repeated reconstruction | The design under comparison |
| **[Karpathy's LLM Wiki][llm-wiki]** | Adaptable workflow pattern | Sources and a generated wiki | Delegate cumulative wiki maintenance to an LLM | Closely related compilation approach |
| **[Obsidian][obsidian-storage]** | General-purpose application | Local Markdown notes | Write and navigate connected notes | Can view and edit a Rensheng repository |
| **[Notion][notion-wiki]** | Workspace application | Pages and databases | Organize knowledge and work | Can remain a source or a separate workspace |
| **[Memex][memex]** | 1945 proposal | Records and associative trails | Extend personal memory and retrieval | Historical reference point |
| **[MyLifeBits][mylifebits]** | Research project, established in 2001 | A lifetime's digital records | Capture, retrieve, and use personal history | Historical comparison for personal archives |

These are different kinds of things: a workflow can run inside an application, and a repository convention can use that application as its interface.

## Modern design matrix

“Workflow-defined” means the user or implementation chooses the behavior; it does not mean the tool cannot support it. Product features depend on configuration and availability.

| Dimension | Rensheng: specified design | [LLM Wiki][llm-wiki] | Obsidian: documented platform | Notion: documented platform |
| --- | --- | --- | --- | --- |
| Primary scope | Private life context; world knowledge kept in a separate Garden | Domain-specific synthesis, including personal life | General-purpose notes and structured views. [Storage][obsidian-storage], [Bases][obsidian-bases] | Knowledge and work within pages, wikis, and databases. [Wikis][notion-wiki], [AI][notion-ai] |
| Persistent artifacts | Small Markdown views; originals elsewhere | Immutable sources, generated Markdown, Agent instructions | Local Markdown files and properties; Bases describes views. [Storage][obsidian-storage], [Bases][obsidian-bases] | Workspace content; Markdown/CSV and other exports are available. [Export][notion-export] |
| Information structure | Personal Context, Captures, Briefs, and separate Knowledge | Chosen for each wiki | Chosen through notes, links, properties, and views. [Backlinks][obsidian-backlinks], [Bases][obsidian-bases] | Chosen through pages, databases, and wiki views. [Wikis][notion-wiki], [AI][notion-ai] |
| Maintenance | External Agents compile focused updates; user-authored statements survive regeneration | LLM ingestion, querying, and consistency checks | Users, plugins, and external file editors can participate. [Storage][obsidian-storage], [Plugins][obsidian-plugins] | Users and configured AI can create or update workspace content. [AI][notion-ai] |
| Evidence and freshness | Source references and verification dates; distinguish current state from history | Retained originals and source-linked synthesis | Evidence conventions are workflow-defined; backlinks expose note relationships. [Backlinks][obsidian-backlinks] | Wiki page ownership and expiring verification are available. [Wikis][notion-wiki] |
| Reading route | Goals and recent updates, relevant Domain, then evidence | Index, then relevant pages | Browse linked notes or file/property views. [Backlinks][obsidian-backlinks], [Bases][obsidian-bases] | Browse wiki views or use workspace and connected-source AI search. [Wikis][notion-wiki], [AI][notion-ai] |
| Personal authority | Accepted Goals, explicit preferences, and observed behavior remain distinct | Set by the chosen schema | Personal decision rules are workflow-defined | Personal decision rules are workflow-defined |

Rensheng rules in this matrix come from [philosophy.md](template/philosophy.md) and [AGENTS.md](template/AGENTS.md). A Markdown convention does not enforce permissions, guarantee correct interpretation, or make an unattended compiler exist.

## How to read the differences

### LLM Wiki: substantial overlap, a more specific contract

Karpathy explicitly includes personal goals, health, and psychology. The gist also describes using Obsidian alongside the Agent. It is a pattern to adapt, rather than a single packaged implementation. [Source][llm-wiki]

Our interpretation is that Rensheng specializes this approach with a defined contract for private life context: what belongs in each view, which statements remain the user's authority, what needs source evidence, and what should stay outside the repository.

The distinction concerns what the structure maintains: accumulated understanding or the person's continuing situation. Both approaches can use domain files. See the [open problems](#open-problems-from-records-and-knowledge-to-a-life-model) below for the responsibilities a life-specific workflow must define.

### Obsidian: a compatible interface

Obsidian already provides local Markdown storage and reflects edits made by other tools. A private Rensheng directory can therefore be opened as a vault while an external Agent updates its files. No Rensheng-specific Obsidian plugin is required for basic reading and editing. This is a compatibility inference from the file model, not a tested integration claim. [Storage][obsidian-storage]

Backlinks and Bases can provide additional navigation or views. Rensheng does not require the user to maintain properties, a graph, or a particular note-taking method. Local files and extensibility are shared foundations, not unique Rensheng inventions. [Backlinks][obsidian-backlinks], [Bases][obsidian-bases], [Plugins][obsidian-plugins]

### Notion: overlapping capabilities, a different storage boundary

Notion has wiki ownership and verification as well as AI that can search connected sources and modify pages or databases. It should not be characterized as requiring all maintenance to be manual. [Wikis][notion-wiki], [AI][notion-ai]

The boundary relevant here is that Rensheng's context is directly readable as ordinary files across Agents. Notion operates on workspace content and offers exports; its documentation notes that re-uploading an export does not instantly reconstruct the workspace. Using Notion as a source is compatible with Rensheng's design, but that does not establish an implemented synchronization path. [Export][notion-export]

## The boundaries Rensheng makes explicit

These are project choices, not capabilities that other PKM systems are incapable of implementing. They are specified in the [philosophy](template/philosophy.md) and the [template guides](template/README.md).

| Distinction | Rensheng convention | Practical consequence |
| --- | --- | --- |
| Personal Context / Knowledge | Private facts about the person live here; general understanding lives in a separate Garden | A current work role and an explanation of the project's technology have different homes |
| Capture / durable preference | Saving an item records attention at a moment; interests can be queried from history | A bookmark does not automatically become a personality label |
| Suggestion / accepted Goal | The person decides which proposed goals become authoritative | Repeated activity alone does not establish a long-term intention |
| Original evidence / generated view | Preserve originals in their source systems or existing stores; keep source-linked summaries here | A summary can be revised without discarding its evidence or the user's wording |
| Current state / history | State when a condition was verified; retain meaningful changes separately | An old statement or recently edited file is not automatically current truth |
| Brief / durable context | A Brief serves a time and purpose; current facts have their own Domain pages | Yesterday's recommendation does not silently become today's commitment |
| Procedure / execution record | Routine pages explain how; execution apps retain actual occurrences and records | A checklist or missing entry does not prove what happened |

## The same information, different responsibilities

The examples below illustrate the proposed division of responsibility; they are not personal data or implemented automation guarantees.

| Situation | Original evidence | Rensheng view | Another tool's role |
| --- | --- | --- | --- |
| A subscription is cancelled but access continues | Billing page and cancellation confirmation | `money/subscriptions.md`: confirmed state, access end, source | The service handles cancellation; an execution app can track follow-up |
| A conversation leaves a response pending | Original message or meeting note | `people/alice.md`: relationship context and open loop | Messaging app retains the exchange; task tool tracks an actionable follow-up |
| A measurement is recorded | Timestamped value and unit in a recording app or store | Relevant `health/` summary when useful | Recording app captures values; a suitable charting tool shows the time series |
| An article is saved | Original URL or saved copy and save metadata | A Capture, without automatically changing profile or goals | A separate Garden can hold knowledge the user chooses to develop |

See the [money](template/money/README.md), [people](template/people/README.md), [health](template/health/README.md), and [captures](template/captures/README.md) guides for concrete formats.

## Historical context

This is a selective comparison, not a complete PKM history or a linear succession of products. MyLifeBits explicitly identifies Memex as an inspiration; the connections to Rensheng below are our interpretation. [MyLifeBits paper][mylifebits-paper]

| Reference | Original emphasis | Connection to Rensheng | Different implementation or focus |
| --- | --- | --- | --- |
| **Memex — 1945** | A proposed microfilm-based personal library, with annotations and associative trails between records. [Bush][memex] | Memory can be supported by retraceable relationships, not just retained items | Rensheng uses files and external Agents to maintain selected current context |
| **MyLifeBits — 2001 project; 2003 paper** | A broad personal archive using database features, typed links, annotations, queries, reports, and temporal navigation. [Project][mylifebits], [Paper][mylifebits-paper] | Preserve evidence and make history useful; retrieve through time and relationships | Rensheng emphasizes a small layer of reusable current context, with original archives outside its Markdown views |

MyLifeBits already addressed retrieval and organization, not merely storage. Its 2003 paper describes saved queries replacing some manual collections, related-item navigation, and suggested links. Reducing filing effort and organizing by query therefore have clear precedents. Rensheng's contribution should be evaluated as a particular combination of responsibilities and conventions, not as the invention of personal digital memory. [Paper][mylifebits-paper]

## Open problems: from records and knowledge to a life model

The following separates documented research observations from Rensheng's design hypotheses. The cited work does not establish a single cause of MyLifeBits' adoption outcomes, or justify treating the research project itself as a failure.

### MyLifeBits: the remaining cost of organization

The expanded 2006 report describes a remaining burden even when classifications and labels are available: users still become a "filing clerk" who annotates their material. The authors call for more automatic organization and capture that does not interrupt everyday life. [Report, organization discussion, PDF p. 9][mylifebits-report]

The same report discusses a Health Memex and future agents that act on a person's state. These were recognized research directions, not evidence of a completed life-management system. [Report, appendix on health and agents, PDF pp. 16–17][mylifebits-report]

The historical lesson we draw is the continuing cost of turning retained records into usable personal state. The absence of modern LLMs alone is not an established explanation: the earlier system already automated parts of retrieval and organization, as described above.

### LLM Wiki: a life-specific contract still has to be defined

LLM Wiki's lint workflow already addresses contradictions and stale claims, and its schema can be adapted. [Source][llm-wiki]

Our interpretation is that a knowledge-centered workflow needs additional decisions when used as a life model. These are responsibilities for its chosen schema, not proof that the pattern cannot support them:

| Challenge when applying a wiki to personal life | Rensheng's specified response | What still needs validation |
| --- | --- | --- |
| A correct historical statement may no longer describe the present | Keep verified current state, relevant changes, and evidence distinguishable | Superseded claims stop appearing as current; missing evidence stays unknown |
| A plausible interpretation can be mistaken for the person's intention | Separate observed behavior, Agent suggestions, and accepted Goals | User corrections and explicit statements survive later compilation |
| More topic pages can increase the amount to navigate or review | Maintain focused life-domain views; retrieve wider history only when needed | Relevant context remains easy to find as sources grow |
| Automated editing can move work from filing into checking and repair | Use small, source-linked updates and preserve user-authored wording | Total user effort decreases, including review and correction |

These responses follow the [Agent guidelines](template/AGENTS.md); their effectiveness is a design goal, not a demonstrated advantage over LLM Wiki.

### Design hypothesis: different information needs different update rules

Our hypothesis is that a personal system becomes harder to maintain when world knowledge, evidence of events, and the person's current situation are treated as interchangeable. Linking them is useful. Their meaning, authority, and update rules need to remain distinct. This is a risk to test in Rensheng as well, not a documented cause of MyLifeBits' outcomes.

| Information role | Fictional subscription example | Update responsibility |
| --- | --- | --- |
| Knowledge about the world | How a service works and how its plans compare | Revise understanding when sources change; keep it in the separate Garden |
| Evidence of an event | An invoice or cancellation confirmation | Retain the original and its date; reference it from the compiled view |
| Personal state | Which plan is active, whether renewal is cancelled, and when access ends | Update from relevant evidence; retain verification dates and unresolved uncertainty |

An old invoice does not establish an active subscription today. Reading a service comparison does not establish a purchase or an intention to subscribe. The [money guide](template/money/README.md) applies these distinctions to the current personal view.

`people/`, `health/`, `money/`, and the other life domains provide stable entrypoints for recurring questions about the person. Within them, the useful distinctions include relationships, conditions, obligations, intentions, and procedures. The folders alone are not a complete life model, and Rensheng does not require a universal ontology. For example, a [person page](template/people/README.md) maintains the relationship and unresolved exchanges; it need not grow into an encyclopedia entry about that person.

### What LLMs change, and what remains Rensheng's responsibility

The opportunity is to delegate interpretation and filing to external Agents while maintaining an explicit structure. Rensheng's core does not perform inference. Source-backed views and conventions let different Agents maintain and read the same personal model.

Automation must preserve the distinction between a recorded event, an interpretation, and a user decision. Evaluate the design by the effort needed to recover context, correct mistakes, and keep current state reliable. A larger archive or a richer wiki alone does not demonstrate that everyday life has become easier.

## Current implementation and intended behavior

This distinction matters when comparing Rensheng with established applications.

| Area | Status at the reviewed revision | What this comparison does not claim |
| --- | --- | --- |
| Private repository layout | Template, Domain guides, profile placeholders, and Agent rules are present. [Template](template/README.md) | A completed personal database ships with the template |
| Agent workflows | Reusable Skills exist, including initial backfill. [Backfill](template/.agents/skills/rensheng-backfill/SKILL.md) | Every connector is available, or updates run continuously by themselves |
| Reading and search | The design uses existing Agent file tools. [Philosophy](template/philosophy.md#15-file-based-retrieval-model) | A dedicated Rensheng CLI or MCP server is required |
| Original-data storage | Originals remain in existing systems; a local raw store is planned. [Philosophy](template/philosophy.md#12-internal-storage-planned) | The planned shared raw store and complete ingestion pipeline are implemented |
| Execution and recording | The repository contains a separately documented OpenBrief implementation. [OpenBrief](docs/openbrief.md) | All planned life-recording, PWA, and export workflows are implemented by the template |
| Effort and reliability | Lower upkeep and better continuity are design goals | This comparison proves reduced effort, automatic correctness, or improved outcomes |

The design is useful only if it reduces repeated explanation and reconstruction without creating another maintenance obligation. That remains a property to verify in actual use.

## Primary sources

- Andrej Karpathy, [LLM Wiki][llm-wiki], idea file created April 4, 2026. The comparison uses the author's document, not third-party implementations or comments.
- Obsidian Help: [How Obsidian stores data][obsidian-storage], [Backlinks][obsidian-backlinks], [Introduction to Bases][obsidian-bases], and [Community plugins][obsidian-plugins].
- Notion Help: [Wikis and verified pages][notion-wiki], [What is Notion AI?][notion-ai], and [Export your content][notion-export].
- Vannevar Bush, [As We May Think][memex], *The Atlantic*, July 1945.
- Microsoft Research, [MyLifeBits project][mylifebits], established November 2, 2001.
- Jim Gemmell, Roger Lueder, and Gordon Bell, [The MyLifeBits Lifetime Store][mylifebits-paper], ETP 2003.
- Jim Gemmell, Gordon Bell, and Roger Lueder, [MyLifeBits: A Personal Database for Everything][mylifebits-report], MSR-TR-2006-23, February 20, 2006. Expanded technical report of the January 2006 CACM article; see the organization discussion and the appendix on health and agents.
- Rensheng: [philosophy](template/philosophy.md), [Agent guidelines](template/AGENTS.md), and [template documentation](template/README.md), at the revision identified above.

[llm-wiki]: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
[obsidian-storage]: https://help.obsidian.md/Files+and+folders/How+Obsidian+stores+data
[obsidian-backlinks]: https://help.obsidian.md/Plugins/Backlinks
[obsidian-bases]: https://help.obsidian.md/bases
[obsidian-plugins]: https://help.obsidian.md/Extending+Obsidian/Community+plugins
[notion-wiki]: https://www.notion.com/help/wikis-and-verified-pages
[notion-ai]: https://www.notion.com/help/notion-ai-faqs
[notion-export]: https://www.notion.com/help/export-your-content
[memex]: https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/
[mylifebits]: https://www.microsoft.com/en-us/research/project/mylifebits/
[mylifebits-paper]: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/etp2003.pdf
[mylifebits-report]: https://www.hcitang.org/uploads/Teaching/2006-gemmell-mylifebits.pdf
