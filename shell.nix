let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.mkShellNoCC {
  packages = with pkgs; [
    # General packages
    sqlite
    python312

    # Python packages
    (pkgs.python3.withPackages (python-pkgs: [
      # python-pkgs.pandas
      python-pkgs.requests
      python-pkgs.flask
      python-pkgs.gunicorn
    ]))

  ];
}
