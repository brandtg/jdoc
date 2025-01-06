import pytest
import tempfile
import os
import subprocess

TEST_POM = r"""
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.github.brandtg</groupId>
    <artifactId>jdoc-test</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>
    <name>jdoc-test</name>
    <url>http://maven.apache.org</url>
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <java.version>21</java.version>
    </properties>
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.1</version>
                <configuration>
                    <source>${java.version}</source>
                    <target>${java.version}</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
    <dependencies>
        <dependency>
            <groupId>commons-io</groupId>
            <artifactId>commons-io</artifactId>
            <version>2.18.0</version>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.11</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
"""


@pytest.fixture
def simple_maven_project():
    with tempfile.TemporaryDirectory() as basedir:
        pomfile = os.path.join(basedir, "pom.xml")
        repodir = os.path.join(basedir, ".repo")
        with open(pomfile, "w") as f:
            f.write(TEST_POM)
        subprocess.check_call(
            [
                "mvn",
                "-f",
                pomfile,
                "dependency:resolve",
                "-Dclassifier=javadoc",
                f"-Dmaven.repo.local={repodir}",
            ],
            stdout=subprocess.DEVNULL,
        )
        yield dict(
            pomfile=pomfile,
            basedir=basedir,
            repodir=repodir,
        )


def test_index_maven(simple_maven_project):
    output = os.path.join(simple_maven_project["basedir"], "jdoc")
    subprocess.check_call(
        [
            "bin/jdoc",
            "--debug",
            "--index",
            "--maven_repo",
            simple_maven_project["repodir"],
            "--gradle_repo",
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
