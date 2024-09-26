import React from "react";
import {Card, CardHeader, CardBody, CardFooter} from "@nextui-org/card";

interface CardProps {
    title: string;
    children: React.ReactNode;
}

const InfoCard: React.FC<CardProps> = ({ title,  children }) => {
  return (
    <Card>
      <CardHeader>
        <p className="text-xl">{title}</p>
      </CardHeader>
      <CardBody>
        {children}
      </CardBody>
      <CardFooter>
        <p className="text-l italic">Source: World Health Organization's data and statistics</p>
      </CardFooter>
    </Card>
  )
}

export default InfoCard