from setuptools import find_packages, setup

E_DASH_DOT = '-e .'
README_PATH = "README.md"
REQUIREMENTS_FILE_PATH = "requirements.txt"

def get_requirements(filename: str) -> list:
    """
    Get package name to install dependencies `requirements.txt`

    Args:
        filename: str -> filename for requirements
    Results:
        requirements: List -> list of name of package
    """
    try:
        with open(filename) as file_handler:
            requirements = file_handler.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if E_DASH_DOT in requirements:
            requirements.remove(E_DASH_DOT)
    except FileNotFoundError as err:
        print(f'[ERROR] requirements not found')
        requirements = ''
    return requirements

def get_readme(filename: str) -> str:
    """
    Get description and overview about package from `README.md` file
    Args: 
        filename: str -> filename of file which gives detail description of pacage for end user
    Return:
        str: A long description abot pacage ehich is in markup text
    """
    try:
        with open(filename) as file_handler:
            content = file_handler.read()
    except FileExistsError as err:
        print(f"[ERROR] No README.md file found for long description")
        content = ''
    return content

setup(
    name="text-summarization",
    version="0.0.21",
    author="realsanjeev",
    author_email="realsanjeev1@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(REQUIREMENTS_FILE_PATH),
    description="Text Summerization using Python",
    long_description=get_readme(README_PATH),
)