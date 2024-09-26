import React from 'react';
import { list } from 'postcss';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface Chart {
    year: number;
    female: number;
    male: number;
}

interface HealthLineChartProps {
    data: Chart[];
    YDomain?: number[];
    colorFM: string;
    colorML: string;
}


const HealthLineChart: React.FC<HealthLineChartProps> = ({data, YDomain, colorFM, colorML}) => {
    return (
        <ResponsiveContainer className="pr-8" width="100%" height={400}>
            <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis domain={YDomain} allowDataOverflow/>
                <Tooltip />
                <Legend />
                {/* Linie für Frauen */}
                <Line type="monotone" dataKey="female" stroke={colorFM} name="Female" />
                {/* Linie für Männer */}
                <Line type="monotone" dataKey="male" stroke={colorML} name="Male" />
            </LineChart>
        </ResponsiveContainer>
    )
}

export default HealthLineChart