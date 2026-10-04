name: Update Ragnarok WOE RSS Feed

on:
  schedule:
    - cron: "*/15 * * * *"

  workflow_dispatch:

permissions:
  contents: write

jobs:
  update-feed:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v5

      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Generate RSS feed
        env:
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
        run: |
          python generate_feed.py

      - name: Check for changes
        id: changes
        run: |
          if git diff --quiet feed.xml; then
            echo "changed=false" >> "$GITHUB_OUTPUT"
          else
            echo "changed=true" >> "$GITHUB_OUTPUT"
          fi

      - name: Commit updated feed
        if: steps.changes.outputs.changed == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add feed.xml
          git commit -m "Update Ragnarok WOE RSS feed"
          git push
