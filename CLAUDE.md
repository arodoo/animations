applyTo: '**'

## Key Principles for this codebase
The main idea os to have a farm of reusable animations. This means, a complex escene should always be built by combining simple, reusable animations. 
iNVESTIGATE THE FILE STRUCTURE BEFORE TO START CODING. 

## Key principles for launchers (IMPORTANT)
Launchers are files I can easily modify while editing the escene. Separe timing of the animations in variables and set them at the launcher. This way, I can easily modify the timing of the escene without having to open each animation file.

Code Quality Rules
Production-ready code only (no TODO, FIXME, or commented-out code)
Follow DDD, SOLID, Clean Architecture
Descriptive naming
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
Split proactively, not reactively
Keep each file focused on ONE responsibility

Respond in a technical and direct manner. Omit introductions, conclusions, and polite phrases. 