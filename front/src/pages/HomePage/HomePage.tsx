import { TobaccoCard } from "components/TobaccoCard";
import {
    BannerStyled,
    TobaccosStyled,
    ContentStyled,
    MainPageStyled,
    TableStyled,
} from "pages/HomePage/HomePage.style";
import React, { useCallback, useEffect } from "react";
import { useNavigate } from "react-router";
import { useAppDispatch, useAppSelector } from "store";
import { getTobaccoListAction } from "store/tobaccos/tobaccos.action";

export const HomePage: React.FC = () => {
    const dispatch = useAppDispatch();
    const { tobaccos } = useAppSelector((store) => store.tobacco);

    useEffect(() => {
        if (!tobaccos?.length) {
            console.log("use effect");
            dispatch(getTobaccoListAction());
        }
    }, [dispatch, tobaccos]);

    const navigate = useNavigate();
    const handleCardClick = useCallback(
        (id: number) => {
            navigate(`/tobaccos/${id}`);
        },
        [navigate]
    );
    return (
        <MainPageStyled>
            <ContentStyled>
                <h1>Табачная</h1>
                <h3>Выберете сигаретки</h3>
                <TableStyled>
                    <BannerStyled>Купите снюс от абобы и получите чаппалах бесплатно!</BannerStyled>

                    <TobaccosStyled>
                        {tobaccos?.map((tobacco) => (
                            <TobaccoCard
                                key={tobacco.id}
                                tobacco={tobacco}
                                onClick={() => handleCardClick(Number(tobacco.id))}
                            />
                        ))}
                    </TobaccosStyled>
                </TableStyled>
            </ContentStyled>
        </MainPageStyled>
    );
};
