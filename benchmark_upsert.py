import time

class MockTable:
    def upsert(self, data, on_conflict=None):
        return MockExecute(data)

class MockExecute:
    def __init__(self, data):
        self.data = data

    def execute(self):
        # Simulate network latency
        time.sleep(0.1)
        return True

class MockSupabaseClient:
    def table(self, table_name):
        return MockTable()

def sync_steps_to_supabase_original(supabase_client, wellness_records):
    for record in wellness_records:
        entry_date = record.get("id")
        steps = record.get("steps")
        if entry_date and steps is not None:
            supabase_client.table("macro_logs").upsert({
                "date": entry_date,
                "steps": int(steps)
            }, on_conflict="date").execute()

def sync_steps_to_supabase_optimized(supabase_client, wellness_records):
    upsert_data = []
    for record in wellness_records:
        entry_date = record.get("id")
        steps = record.get("steps")
        if entry_date and steps is not None:
            upsert_data.append({
                "date": entry_date,
                "steps": int(steps)
            })

    if upsert_data:
        supabase_client.table("macro_logs").upsert(upsert_data, on_conflict="date").execute()

def main():
    print("Running Benchmark: N+1 Query vs Bulk Upsert")
    print("=" * 50)

    records = [{"id": f"2023-10-{i:02d}", "steps": i * 1000} for i in range(1, 15)]
    client = MockSupabaseClient()

    print(f"Testing with {len(records)} records (simulating 0.1s network latency per request)")

    # Original
    start_time = time.time()
    sync_steps_to_supabase_original(client, records)
    original_time = time.time() - start_time
    print(f"Original (N+1): {original_time:.4f} seconds")

    # Optimized
    start_time = time.time()
    sync_steps_to_supabase_optimized(client, records)
    optimized_time = time.time() - start_time
    print(f"Optimized (Bulk): {optimized_time:.4f} seconds")

    improvement = original_time - optimized_time
    speedup = original_time / optimized_time if optimized_time > 0 else 0
    print(f"Improvement: {improvement:.4f} seconds faster ({speedup:.2f}x speedup)")

if __name__ == "__main__":
    main()
