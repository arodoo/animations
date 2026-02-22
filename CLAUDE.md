applyTo: '**'

## Key Principles for this codebase
The main idea os to have a farm of reusable animations. This means, a complex escene should always be built by combining simple, reusable animations. 

MUSTS
Quality over speed is a must always

Code Quality Rules
Production-ready code only (no TODO, FIXME, or commented-out code)
Follow DDD, SOLID, Clean Architecture
Long-term focus: write code that won't break in 1-2 years
Descriptive naming (e.g. response vs r)
English for code, comments, and vars
When try/catch, catch should always trow the specific error, never be empty

80/60 RULE
MAX: 80L/file, 60char/line (CI@80). JSON exempt. PRE-WRITE: Lines>=70 OR chars>=55? SPLIT NOW. SPLIT: DDD layers (domain/app/infra), 1 concern/file NEVER: Compress, defer, ignore DDD MAX: Entity(50L) ValueObj(30L) Service(60L) UseCase(55L) DTO(40L) Mapper(45L) Repo(60L) Adapter(55L)

NEVER
Create files over 80 lines "temporarily"
Assume you'll refactor later
Compress code to fit (remove spaces, shorten names)
Ignore limits because "it's just a few lines"
ALWAYS
Count lines as you write
Split proactively, not reactively
Keep each file focused on ONE responsibility
Respect the 60/60 buffer (CI fails at 80/80)