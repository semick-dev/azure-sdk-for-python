import os
from ci_tools.build import discover_targeted_packages


root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", ".."))


from ci_tools.environment_exclusions import MYPY_OPT_OUT, PYLINT_OPT_OUT, PYRIGHT_OPT_OUT, TYPE_CHECK_SAMPLES_OPT_OUT, VERIFYTYPES_OPT_OUT 

PYPROJ_TEMPLATE = """
[tool.azure-sdk-build]
{}
"""

all_pkgs = discover_targeted_packages("azure*", root_dir)

for pkg in all_pkgs:
    package_name = os.path.basename(pkg)
    pyproject_path = os.path.join(pkg, "pyproject.toml")

    package_exclusions = []

    if package_name in MYPY_OPT_OUT:
        package_exclusions.append(f"mypy = false")

    if package_name in PYLINT_OPT_OUT:
        package_exclusions.append(f"pylint = false")

    if package_name in PYRIGHT_OPT_OUT:
        package_exclusions.append(f"pyright = false")

    if package_name in TYPE_CHECK_SAMPLES_OPT_OUT:
        package_exclusions.append(f"type_check_samples = false")

    if package_name in VERIFYTYPES_OPT_OUT:
        package_exclusions.append(f"verifytypes = false")
    
    if not os.path.exists(pyproject_path):
        with open(pyproject_path, "w") as f:
            content = PYPROJ_TEMPLATE.format(os.linesep.join(package_exclusions))
    else:
        print(f"Skipping {package_name}")
