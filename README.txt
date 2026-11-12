FOOTBALL PENALTY - ANDROID APK PROJECT

Files:
- main.py: Kivy football penalty shootout game
- buildozer.spec: Android package settings
- .github/workflows/build.yml: GitHub Actions cloud build recipe

To build using only an Android phone:
1. Sign in or create an account at https://github.com
2. Create a NEW PUBLIC repository named football-penalty.
3. Upload the contents of this folder to the repository root.
   Make sure main.py and buildozer.spec are at the top level.
   Also upload the .github/workflows/build.yml file in that exact folder path.
4. Open the repository's Actions tab and enable Actions if prompted.
5. Choose "Build Football APK" then "Run workflow".
6. Wait for the workflow to finish successfully.
7. Open the completed run, find Artifacts, and download football-penalty-apk.
8. Extract the downloaded ZIP and install the APK. Android may ask you to allow
   installs from your browser or file manager.

Note: GitHub's cloud runner performs the Linux build. The first build can take
several minutes. This project is a Kivy rewrite; the original Pygame script is
not directly packaged by this project.
