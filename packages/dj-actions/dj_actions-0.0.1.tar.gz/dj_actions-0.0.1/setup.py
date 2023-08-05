import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dj_actions",
    version="0.0.1",
    author="AppointmentGuru",
    author_email="tech@appointmentguru.co",
    description="A framework for performating complex actions on objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/SchoolOrchestration/libs/dj-actions",
    packages=['actions'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
