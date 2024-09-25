import InfoCard from '../components/Card'

const Home = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4">
      <InfoCard title="Card 1" description="Dies ist die erste Karte." />
      <InfoCard title="Card 2" description="Dies ist die zweite Karte." />
      <InfoCard title="Card 3" description="Dies ist die dritte Karte." />
    </div>
  )
}

export default Home