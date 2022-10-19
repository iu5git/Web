import { TOBACCO } from "constants/tobaccos";
import { ButtonStyled, TobaccoPageStyled } from "pages/TobaccoPage/TobaccoPage.style";
import React from "react";
import { useParams } from "react-router";

import { TobaccoPageProps } from "./TobaccoPage.types";

export const TobaccoPage: React.FC<TobaccoPageProps> = () => {
    const params = useParams<{ id: string }>();

    return (
        <TobaccoPageStyled>
            <h1>{TOBACCO.find((tobacco) => tobacco.id === Number(params.id))?.title}</h1>
            <h2>${TOBACCO.find((tobacco) => tobacco.id === Number(params.id))?.price}</h2>
            <ButtonStyled
                onClick={() => {
                    alert("Куплено!");
                }}
            >
                Купить
            </ButtonStyled>
        </TobaccoPageStyled>
    );
};
