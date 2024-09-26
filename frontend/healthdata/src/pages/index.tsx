import { useEffect, useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Autocomplete, AutocompleteItem } from "@nextui-org/autocomplete";
import InfoCard from '@/components/Card';
import HealthLineChart from '@/components/HealthLineChart';

interface Chart {
    year: number;
    female: number;
    male: number;
}

const Home = () => {
    const [selCountry, setSelCountry] = useState<string>('DEU');
    const [dataLE, setDataLE] = useState<Chart[]>([]);
    const [dataOP, setDataOP] = useState<Chart[]>([]);
    const [dataHP, setdataHP] = useState<Chart[]>([]);
    const [dataDP, setdataDP] = useState<Chart[]>([]);
    const [countries, setCountries] = useState<Record<string, string>>({});

    // Abrufen der verfügbaren Länder
    useEffect(() => {
        axios.get<Record<string, string>>('http://localhost:8000/countries')
        .then((response) => {
            setCountries(response.data);
        })
        .catch((error) => {
            console.error("Fehler beim Abrufen der Daten", error);
        });
    }, []);

    // Abrufen der Daten
    useEffect(() => {
        // Lebenserwartung
        axios.get<Chart[]>(`http://localhost:8000/life-expectancy?country=${selCountry}`)
        .then((response) => {
            setDataLE(response.data);
        })
        .catch((error) => {
            console.error("Fehler beim Abrufen der Daten", error);
        });

        // Prävalenz für Übergewicht
        axios.get<Chart[]>(`http://localhost:8000/obesity-prevalence?country=${selCountry}`)
        .then((response) => {
            setDataOP(response.data);
        })
        .catch((error) => {
            console.error("Fehler beim Abrufen der Daten", error);
        });

        // Prävalenz für Bluthochdruck
        axios.get<Chart[]>(`http://localhost:8000/hypertension-prevalence?country=${selCountry}`)
        .then((response) => {
            setdataHP(response.data);
        })
        .catch((error) => {
            console.error("Fehler beim Abrufen der Daten", error);
        });

        // Sterbewahrscheinlichkeit an Volkskrankheiten
        axios.get<Chart[]>(`http://localhost:8000/death-probability?country=${selCountry}`)
        .then((response) => {
            setdataDP(response.data);
        })
        .catch((error) => {
            console.error("Fehler beim Abrufen der Daten", error);
        });
    }, [selCountry]); 

    return (
        <div>
            {/* Autocomplete Dropdown für Länder */}
            <Autocomplete
                label="Choose country"
                className='py-4 max-w-sx'
                onSelectionChange={(selectedValue) => setSelCountry(selectedValue as string)}  // Hier wird das ausgewählte Land gesetzt
            >
                {Object.entries(countries).map(([key, value]) => (
                    <AutocompleteItem key={key} value={value}>
                        {value}
                    </AutocompleteItem>
                ))}
            </Autocomplete>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-2 gap-4">
                <InfoCard title="Life expectancy (years)">
                    {/* Liniendiagramm für Männer und Frauen */}
                    <HealthLineChart
                        data={dataLE}
                        YDomain={[40, 90]}
                        colorFM="#8884d8"
                        colorML="#82ca9d"
                    />
                </InfoCard>
                <InfoCard title="Probability (%) of dying between age 30 and exact age 70 from any of cardiovascular disease, cancer, diabetes, or chronic respiratory disease">
                    {/* Liniendiagramm für Männer und Frauen */}
                    <HealthLineChart
                        data={dataDP}
                        colorFM="#9b59b6"
                        colorML="#e67e22"
                    />
                </InfoCard>
                <InfoCard title="Prevalence of obesity among adults (%)">
                    {/* Liniendiagramm für Männer und Frauen */}
                    <HealthLineChart
                        data={dataOP}
                        YDomain={[0, 60]}
                        colorFM="#1abc9c"
                        colorML="#e91e63"
                    />
                </InfoCard>
                <InfoCard title="Prevalence hypertension among adults aged 30-79 (%)">
                    {/* Liniendiagramm für Männer und Frauen */}
                    <HealthLineChart
                        data={dataHP}
                        colorFM="#3498db"
                        colorML="#e74c3c"
                    />
                </InfoCard>
            </div>
        </div>
    );
};

export default Home;
