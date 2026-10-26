NagarSetu — Technology Stack Icons
A visual, supplementary technology-stack reference for NagarSetu. This file is intentionally separate from the repository's existing [`README.md`](./README.md); it does not replace or rewrite the project overview.

The icons below use the supported icon IDs from tandpfun/skill-icons via skillicons.dev. Technologies are ordered by the application's architecture: frontend → backend → storage → retrieval/model runtime → deployment and source control.
1. Frontend
<p align="left">
  <a href="https://skillicons.dev" aria-label="NagarSetu frontend technologies">
    <img src="https://skillicons.dev/icons?i=nextjs,react,ts,tailwind,nodejs,npm&perline=6" alt="Next.js, React, TypeScript, Tailwind CSS, Node.js, npm" />
  </a>
</p>

Technology	Purpose in NagarSetu
Next.js	Frontend application and routing
React	UI component rendering
TypeScript	Frontend type checking
Tailwind CSS	Utility-first styling
Node.js / npm	Frontend tooling and dependency management


2. Backend API
<p align="left">
  <a href="https://skillicons.dev" aria-label="NagarSetu backend technologies">
    <img src="https://skillicons.dev/icons?i=py,fastapi&perline=2" alt="Python and FastAPI" />
  </a>
</p>

Technology	Purpose in NagarSetu
Python	Backend language and RAG orchestration
FastAPI	HTTP API for authentication, chat, and progress
Uvicorn	ASGI application server; no dedicated Skill Icons entry is available
Pydantic	Request/response schema validation; no dedicated Skill Icons entry is available


3. Data storage
<p align="left">
  <a href="https://skillicons.dev" aria-label="NagarSetu database technologies">
    <img src="https://skillicons.dev/icons?i=sqlite,postgres&perline=2" alt="SQLite and PostgreSQL" />
  </a>
</p>

Technology	Status / purpose
SQLite	Used by the current authentication implementation; verify the configured storage path and persistence guarantees before treating it as durable production storage
PostgreSQL	Optional/configuration-driven support exists in the project; do not imply that all account and progress data use PostgreSQL unless the deployment code path confirms it


SQL note: Skill Icons does not list a generic sql icon. These are the database-specific icons for SQLite and PostgreSQL, the SQL database technologies referenced by NagarSetu. Do not add MySQL just to represent SQL; it is not established as a project dependency.
4. Retrieval, embeddings, and LLM providers
<p align="left">
  <a href="https://skillicons.dev" aria-label="NagarSetu model runtime">
    <img src="https://skillicons.dev/icons?i=pytorch&perline=1" alt="PyTorch" />
  </a>
</p>

Technology	Purpose in NagarSetu	Icon availability
ChromaDB	Vector storage and retrieval	No dedicated Skill Icons entry; listed by name rather than represented by an unrelated icon
Sentence Transformers	Embedding model utilities	No dedicated Skill Icons entry
BM25 (rank-bm25)	Keyword-based retrieval	No dedicated Skill Icons entry
Groq API	LLM provider integration	No dedicated Skill Icons entry
Google Gemini API	LLM provider integration	No dedicated Skill Icons entry; the gcp icon represents Google Cloud Platform, not the Gemini API specifically
PyTorch	Model/embedding runtime dependency	pytorch icon available


The supported retrieval and LLM components are written out explicitly because the selected icon catalogue does not provide accurate dedicated icons for every dependency. No unrelated logo is substituted for a missing icon.
5. Hosting and source control
<p align="left">
  <a href="https://skillicons.dev" aria-label="NagarSetu hosting and source-control technologies">
    <img src="https://skillicons.dev/icons?i=cloudflare,git,github&perline=3" alt="Cloudflare, Git, and GitHub" />
  </a>
</p>

Platform / tool	Purpose
Cloudflare Pages	Frontend deployment
Render	Backend deployment; no dedicated Render icon is listed in Skill Icons
Git	Version control
GitHub	Source repository and collaboration


6. Testing and supporting libraries
These are project dependencies or capabilities, but the selected Skill Icons catalogue does not provide a clearly matching dedicated icon for each one:
- pytest — Python test framework.
- httpx — HTTP client used by tests and/or API integration.
- lucide-react — interface icons.
- Framer Motion — frontend animations.
- pydantic — data validation.
Refer to the root [`README.md`](./README.md), frontend/package.json, and requirements.txt for the project overview and dependency declarations.
