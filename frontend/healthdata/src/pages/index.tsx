import { useEffect, useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Autocomplete, AutocompleteItem } from "@nextui-org/autocomplete";

interface LifeExpectancy {
    country: string;
    year: number;
    sex: string;
    value: number;
}

const Home = () => {
    const [selCountry, setSelCountry] = useState<string>('DEU');
    const [data, setData] = useState<LifeExpectancy[]>([]);
    const [countries, setCountries] = useState<string[]>([]);

    // Abrufen der verfügbaren Länder
    useEffect(() => {
        axios.get<string[]>('http://localhost:8000/countries')
        .then((response) => {
            setCountries(response.data);
        })
        .catch((error) => {
            console.error("Fehler beim Abrufen der Daten", error);
        });
    }, []);

    // Abrufen der Lebenserwartungsdaten basierend auf dem ausgewählten Land
    useEffect(() => {
        axios.get<LifeExpectancy[]>(`http://localhost:8000/life-expectancy?country=${selCountry}`)
        .then((response) => {
            setData(response.data);
        })
        .catch((error) => {
            console.error("Fehler beim Abrufen der Daten", error);
        });
    }, [selCountry]); 

    return (
        <div>
            {/* Autocomplete Dropdown für Länder */}
            <Autocomplete
                label="Wähle ein Land aus"
                className='max-w-sx'
                onSelectionChange={(selectedValue) => setSelCountry(selectedValue as string)}  // Hier wird das ausgewählte Land gesetzt
            >
                {countries.map((country) => (
                    <AutocompleteItem key={country} value={country}>
                        {country}
                    </AutocompleteItem>
                ))}
            </Autocomplete>

            {/* Liniendiagramm für Männer und Frauen */}
            <ResponsiveContainer width="100%" height={400}>
                <LineChart data={data.filter(d => d.sex === 'SEX_MLE' || d.sex === 'SEX_FMLE')}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    {/* Linie für Männer */}
                    <Line type="monotone" data={data.filter(d => d.sex === "SEX_MLE")} dataKey="value" stroke="#8884d8" name="Männer" />
                    {/* Linie für Frauen */}
                    <Line type="monotone" data={data.filter(d => d.sex === "SEX_FMLE")} dataKey="value" stroke="#82ca9d" name="Frauen" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default Home;
