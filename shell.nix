let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.mkShell {
  packages = with pkgs; [
    # General packages
    sqlite
    python312

    # Python packages
    (python312.withPackages (pypkgs: with pypkgs; [
        yapf
        flask
        gunicorn
        bcrypt
    ]))

  ];
}
