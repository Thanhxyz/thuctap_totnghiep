from backend.models import TokenAllocation
import asyncpg

async def calculate_vesting_schedule(db: asyncpg.Pool, project_id: int):
    query = "SELECT * FROM token_allocation WHERE project_id = $1"
    allocations = await db.fetch(query, project_id)

    for allocation in allocations:
        total_tokens = allocation['percentage'] / 100 * allocation['total_supply']
        unlocked_tge = total_tokens * allocation['initial_unlock'] / 100
        remaining_tokens = total_tokens - unlocked_tge
        tokens_per_month = remaining_tokens / allocation['vesting_months']
        vesting_date = allocation['launch_date'] + timedelta(days=allocation['cliff_months'] * 30)

        for month in range(1, allocation['vesting_months'] + 1):
            vesting_date += timedelta(days=30)
            query = """
            INSERT INTO vesting_schedule (allocation_id, month_number, unlock_date, unlocked_tokens)
            VALUES ($1, $2, $3, $4)
            """
            await db.execute(query, allocation['allocation_id'], month, vesting_date, tokens_per_month)
