import { TobaccoCardStyled } from "components/TobaccoCard/TobaccoCard.style";
import React from "react";

import { CoffeeCardProps } from "./TobaccoCard.types";

export const TobaccoCard: React.FC<CoffeeCardProps> = ({ tobacco: coffee, ...props }) => {
    return (
        <TobaccoCardStyled {...props}>
            <h2>{coffee.title}</h2>
            <p>${coffee.price}</p>
        </TobaccoCardStyled>
    );
};
