import { useEffect, useState, Dispatch, SetStateAction} from 'react';
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
    const [dataHP, setDataHP] = useState<Chart[]>([]);
    const [dataDP, setDataDP] = useState<Chart[]>([]);
    const [countries, setCountries] = useState<Record<string, string>>({});


    const getChartData = async (url_end: string, setFunc: Dispatch<SetStateAction<Chart[]>>) => {
        axios.get<Chart[]>(`http://localhost:8000/${url_end}?country=${selCountry}`)
        .then((response) => {
            setFunc(response.data);
        })
        .catch((error) => {
            console.error("Fehler beim Abrufen der Daten", error);
        });
    }

    // Abrufen der verfügbaren Länder
    useEffect(() => {
        axios.post('http://localhost:8000/import-data')
        .then(response => {
            console.log('Daten wurden erfolgreich importiert:', response.data);
        })
        .catch(error => {
        console.error('Fehler beim Importieren der Daten:', error);
        });

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
        getChartData("life-expectancy", setDataLE)

        // Prävalenz für Übergewicht
        getChartData("obesity-prevalence", setDataOP)
        
        // Prävalenz für Bluthochdruck
        getChartData("hypertension-prevalence", setDataHP)

        // Sterbewahrscheinlichkeit an Volkskrankheiten
        getChartData("death-probability", setDataDP)

    }, [selCountry]); 

    return (
        <div className='pb-6'>
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
                <InfoCard title="Probability (%) of dying between age 30-70 from any of cardiovascular disease, cancer, diabetes, or chronic respiratory disease">
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
