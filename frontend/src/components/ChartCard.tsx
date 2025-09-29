// frontend/src/components/ChartCard.tsx
"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

interface ChartCardProps {
    title: string;
    data: {date: string; value: number}[];
}

export default function ChartCard({ title, data }: ChartCardProps) {
    return (
        <div className="bg-white shadow rounded-2xl p-4">
            <h2 className="text-lg font-semibold mb-2">{title}</h2>
            <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis />
                        <YAxis />
                        <Tooltip />
                        <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}