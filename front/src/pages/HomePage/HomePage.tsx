import { TobaccoCard } from "components/TobaccoCard";
import { TOBACCO } from "constants/tobaccos";
import {
    BannerStyled,
    TobaccosStyled,
    ContentStyled,
    MainPageStyled,
    TableStyled,
} from "pages/HomePage/HomePage.style";
import React, { useCallback } from "react";
import { useNavigate } from "react-router";

export const HomePage: React.FC = () => {
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
                        {TOBACCO.map((tobacco) => (
                            <TobaccoCard
                                key={tobacco.id}
                                tobacco={tobacco}
                                onClick={() => handleCardClick(tobacco.id)}
                            />
                        ))}
                    </TobaccosStyled>
                </TableStyled>
            </ContentStyled>
        </MainPageStyled>
    );
};
