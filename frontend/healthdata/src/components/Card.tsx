import {Card, CardHeader, CardBody, CardFooter} from "@nextui-org/card";


const InfoCard = ({ title, description }: { title: string, description: string }) => {
  return (
    <Card>
      <CardHeader>
        <p>{title}</p>
      </CardHeader>
      <CardBody>
        {<p>{description}</p>}
      </CardBody>
    </Card>
  )
}

export default InfoCard