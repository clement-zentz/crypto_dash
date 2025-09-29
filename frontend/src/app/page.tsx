// frontend/src/app/dashboard/page.tsx
"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchCryptoData } from "../../lib/api";
import ChartCard from "@/components/ChartCard";

export default function DashboardPage() {
    const { data, isLoading, error } = useQuery({
        queryKey: ["crypto"],
        queryFn: fetchCryptoData,
    });


    if (isLoading) return <p>Loading data...</p>
    if (error) return <p>Error fetching data</p>


    return (
        <div className="grid grid-col-1 md:grid-cols-2 gap-6">
            <ChartCard title="Bitcoin Price (USD)" data={data?.bitcoin} />
            <ChartCard title="Ethereum Price (USD)" data={data?.ethereum} />
        </div>
    );
}