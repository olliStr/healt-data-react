import { useEffect, useState } from 'react';
import axios from 'axios';

interface LifeExpectancy {
    country: string;
    year: number;
    sex: string;
    value: number;
}

const Home = () => {
    const [data, setData] = useState<LifeExpectancy[]>([]);

    useEffect(() => {
        axios.get<LifeExpectancy[]>('http://localhost:8000/life-expectancy')
        .then((response) => {
            setData(response.data);
        })
        .catch((error) => {
            console.error("Fehler beim Abrufen der Daten", error);
        });
    }, [])

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
          {data.map((entry, index) => (
            <div key={index} className="border p-4">
              <h2>{entry.country} - {entry.year}</h2>
              
              <p>{entry.sex}: {entry.value}</p>
            </div>
          ))}
        </div>
      );
    };

export default Home