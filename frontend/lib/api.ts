// frontend/lib/api.ts

export async function fetchCryptoData() {
    const res = await fetch("http://localhost:8000/api/crypto/");
    if (!res.ok) throw new Error("Failed to fetch data");
    return res.json();
}