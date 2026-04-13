{
  description = "Gifmaker Python Application";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {self, nixpkgs}:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgsFor = system: import nixpkgs {inherit system;};
    in {
      packages = forAllSystems (system:
        let
          pkgs = pkgsFor system;
          pythonPackages = pkgs.python3Packages;
        in {
          default = pythonPackages.buildPythonApplication {
            # Nix typically requires a static pname and version,
            # though setup.py will still use your manifest.json internally.
            pname = "gifmaker";
            version = "unstable";

            # Uses the current directory as the source.
            # Ensure your files (including gifmaker/manifest.json) are tracked in git!
            src = ./.;

            # Maps the requirements from your requirements.txt to Nix packages
            propagatedBuildInputs = with pythonPackages; [
              imageio
              imageio-ffmpeg
              pillow
              numpy
              webcolors
              gitpython
            ];

            # Skips testing phase since no tests are defined in setup.py
            doCheck = false;
          };
        });

      devShells = forAllSystems (system:
        let
          pkgs = pkgsFor system;
          pythonPackages = pkgs.python3Packages;
        in {
          # Provides a development environment with all requirements installed
          default = pkgs.mkShell {
            packages = [
              (pkgs.python3.withPackages (ps: with ps; [
                imageio
                imageio-ffmpeg
                pillow
                numpy
                webcolors
                gitpython
              ]))
            ];
          };
        });
    };
}