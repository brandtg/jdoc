import pytest
import tempfile
import os
import subprocess

TEST_BUILD_GRADLE = r"""
plugins {
	id 'java'
	id 'idea'
}

repositories {
	mavenCentral()
}

dependencies {
	implementation 'commons-io:commons-io:2.18.0'
}

idea {
  module {
    downloadJavadoc = true
    downloadSources = true
  }
}
"""


@pytest.fixture
def simple_gradle_project():
    with tempfile.TemporaryDirectory() as basedir:
        buildfile = os.path.join(basedir, "build.gradle")
        repodir = os.path.join(basedir, ".repo")
        with open(buildfile, "w") as f:
            f.write(TEST_BUILD_GRADLE)
        subprocess.check_call(
            [
                "gradle",
                "-g",
                repodir,
                "build",
                "idea",
            ],
            cwd=basedir,
        )
        yield dict(
            buildfile=buildfile,
            basedir=basedir,
            repodir=repodir,
        )


def test_index_gradle(simple_gradle_project):
    output = os.path.join(simple_gradle_project["basedir"], "jdoc")
    subprocess.check_call(
        [
            "bin/jdoc",
            "--debug",
            "--index",
            "--gradle_repo",
            simple_gradle_project["repodir"],
            "--maven_repo",
            "DUMMY",
            "--output",
            output,
        ]
    )
    output = subprocess.check_output(
        ["bin/jdoc", "XmlStreamWriter", "--output", output]
    )
    results = [line.split("\t") for line in output.decode("utf-8").strip().split("\n")]
    assert len(results) > 0
    for result in results:
        assert len(result) == 3  # class, jar, javadoc
        assert "XmlStreamWriter" in result[0]
        assert result[1] == "commons-io-2.18.0-javadoc.jar"
        assert result[2].startswith("file:///")
