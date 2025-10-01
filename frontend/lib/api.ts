// frontend/lib/api.ts

export async function fetchCryptoData(days = 7) {
    const url = `http://localhost:8000/api/crypto/?refresh=true&days=${days}`;
    const res = await fetch(url, { next: { revalidate: 0 } });
    if (!res.ok) throw new Error("Failed to fetch data");
    return res.json();
}