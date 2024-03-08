import PG from "pg";

const user = "";
const pass = "";
const port = 5432;
const server = "localhost";
const db = "blackjack";

const connectionString = `postgres://${user}:${pass}@${server}:${port}/${db}`;

const pool = new PG.Pool({ connectionString });

export async function insertGameState(payload: string) {
  await pool.query("insert into history(state) VALUES($1)", [payload]);
}

export async function readGameState() {
  const res = await pool.query("select * from history");
  return res.rows;
}
