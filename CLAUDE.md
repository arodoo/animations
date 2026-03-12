applyTo: '**'

## Key Principles for this codebase
The main idea os to have a farm of reusable animations. This means, a complex escene should always be built by combining simple, reusable father animations located out of the animation folder, but in a separated, reusable and scallable folders . 
iNVESTIGATE THE FILE STRUCTURE BEFORE TO START CODING. 

## Key principles for launchers (IMPORTANT)
Set variables suchs as duration of each part of the animation, colors, brightness, etc in the launcher.py so I can easily change them.

Code Quality Rules
Production-ready code only (no TODO, FIXME, or commented-out code)
Follow DDD, SOLID, Clean Architecture
Descriptive naming
English for code, comments, and vars
When try/catch, catch should always trow the specific error, never be empty

80/60 RULE
MAX: 80L/file, 60char/line (CI@80). JSON exempt. PRE-WRITE: Lines>=70 OR chars>=55? SPLIT NOW. SPLIT: DDD layers (domain/app/infra), 1 concern/file NEVER: Compress, defer, ignore DDD MAX: Entity(50L) ValueObj(30L) Service(60L) UseCase(55L) DTO(40L) Mapper(45L) Repo(60L) Adapter(55L)

# !ALWAYS ANIMATE USING 'Disney's 12 Principles of Animation'¡