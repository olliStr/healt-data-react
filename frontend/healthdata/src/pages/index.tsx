import { useEffect, useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Autocomplete, AutocompleteItem } from "@nextui-org/autocomplete";
import InfoCard from '@/components/Card';

interface LifeExpectancy {
    year: number;
    female: number;
    male: number;
}

interface ObesityPrev {
    year: number;
    female: number;
    male: number;
}

const Home = () => {
    const [selCountry, setSelCountry] = useState<string>('DEU');
    const [dataLE, setDataLE] = useState<LifeExpectancy[]>([]);
    const [dataOP, setDataOP] = useState<ObesityPrev[]>([]);
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
        axios.get<LifeExpectancy[]>(`http://localhost:8000/life-expectancy?country=${selCountry}`)
        .then((response) => {
            setDataLE(response.data);
        })
        .catch((error) => {
            console.error("Fehler beim Abrufen der Daten", error);
        });

        // Prävalenz für Übergewicht
        axios.get<LifeExpectancy[]>(`http://localhost:8000/obesity-prevalence?country=${selCountry}`)
        .then((response) => {
            setDataOP(response.data);
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
                    <InfoCard title="Life expectancy (years)" footer="Source: WHO GHO">
                        {/* Liniendiagramm für Männer und Frauen */}
                        <ResponsiveContainer className="pr-8" width="100%" height={400}>
                            <LineChart data={dataLE}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="year" />
                                <YAxis domain={[30, 90]} allowDataOverflow/>
                                <Tooltip />
                                <Legend />
                                {/* Linie für Frauen */}
                                <Line type="monotone" dataKey="female" stroke="#8884d8" name="Frauen" />
                                {/* Linie für Männer */}
                                <Line type="monotone" dataKey="male" stroke="#82ca9d" name="Männer" />
                            </LineChart>
                        </ResponsiveContainer>
                    </InfoCard>
                    <InfoCard title="Prevalence of obesity among adults (%)" footer="Source: WHO GHO">
                        {/* Liniendiagramm für Männer und Frauen */}
                        <ResponsiveContainer className="pr-8" width="100%" height={400}>
                            <LineChart data={dataOP}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="year" />
                                <YAxis domain={[0, 60]} allowDataOverflow/>
                                <Tooltip />
                                <Legend />
                                {/* Linie für Frauen */}
                                <Line type="monotone" dataKey="female" stroke="#8884d8" name="Frauen" />
                                {/* Linie für Männer */}
                                <Line type="monotone" dataKey="male" stroke="#82ca9d" name="Männer" />
                            </LineChart>
                        </ResponsiveContainer>
                    </InfoCard>
                </div>



        </div>
    );
};

export default Home;
