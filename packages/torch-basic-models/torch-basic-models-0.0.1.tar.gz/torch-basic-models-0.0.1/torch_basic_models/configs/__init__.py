from pathlib import Path

import json_schema_to_class

current_dir: Path = Path(__file__).parent
build_dir: Path = current_dir / 'build'
build_dir.mkdir(exist_ok=True, parents=True)

generate_modules = []
for schema_path in current_dir.glob('../schema/*.yaml'):
    output_path = build_dir / schema_path.with_suffix('.py').name
    json_schema_to_class.generate_file(schema_path=schema_path, output_path=output_path, lazy=True)
    generate_modules.append(f'from .{output_path.stem} import *')

generate_modules.sort()
init_content = '\n'.join(generate_modules)
init_path = build_dir / '__init__.py'

if not init_path.exists() or open(str(init_path)).read() != init_content:
    with open(str(init_path), 'w') as f:
        f.write(init_content + '\n')

if __name__ != '__main__':
    from .build import *  # noqa: F403
