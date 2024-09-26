import React from "react";
import {Card, CardHeader, CardBody, CardFooter} from "@nextui-org/card";

interface CardProps {
    title: string;
    children: React.ReactNode;
    footer: string;
}

const InfoCard: React.FC<CardProps> = ({ title,  children, footer }) => {
  return (
    <Card>
      <CardHeader>
        <p>{title}</p>
      </CardHeader>
      <CardBody>
        {children}
      </CardBody>
      <CardFooter>
        <p>{footer}</p>
      </CardFooter>
    </Card>
  )
}

export default InfoCard