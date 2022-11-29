import { ButtonStyled, TobaccoPageStyled } from "pages/TobaccoPage/TobaccoPage.style";
import React, { useEffect } from "react";
import { useParams } from "react-router";
import { useAppDispatch, useAppSelector } from "store";
import { getTobaccoByIdAction } from "store/tobaccos/tobaccos.action";

import { TobaccoPageProps } from "./TobaccoPage.types";

export const TobaccoPage: React.FC<TobaccoPageProps> = () => {
    const params = useParams<{ id: string }>();
    const dispatch = useAppDispatch();
    const { tobacco } = useAppSelector((store) => store.tobacco);

    useEffect(() => {
        if (!tobacco) {
            dispatch(getTobaccoByIdAction(String(params.id)));
        }
    }, [dispatch, params.id, tobacco]);

    return (
        <TobaccoPageStyled>
            <h1>{tobacco?.name}</h1>
            <h2>${tobacco?.price}</h2>
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
