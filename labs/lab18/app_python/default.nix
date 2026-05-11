{ pkgs ? import <nixpkgs> {} }:

pkgs.python3Packages.buildPythonApplication rec {
  pname = "devops-info-service";
  version = "1.0.0";

  src = ./.;

  format = "other";

  propagatedBuildInputs = with pkgs.python3Packages; [
    flask
    prometheus-client
  ];

  nativeBuildInputs = [
    pkgs.makeWrapper
  ];

  installPhase = ''
    mkdir -p $out/bin

    cp app.py $out/bin/devops-info-service

    chmod +x $out/bin/devops-info-service

    wrapProgram $out/bin/devops-info-service \
      --set PYTHONUNBUFFERED 1 \
      --prefix PYTHONPATH : "$PYTHONPATH"
  '';

  meta = with pkgs.lib; {
    description = "DevOps Info Service";
    platforms = platforms.all;
  };
}
