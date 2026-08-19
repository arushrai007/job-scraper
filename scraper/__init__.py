from scraper.pacing import polite_delay

if __name__ == "__main__":
    # Simulate 3 pulls in a row, as if this were a scheduled job running repeatedly
    for i in range(3):
        print(f"\n--- Pull #{i+1} ---")
        data = fetch_jobs()
        print(f"Fetched {len(data['data'])} jobs")

        if i < 2:  # don't wait after the last pull
            polite_delay()