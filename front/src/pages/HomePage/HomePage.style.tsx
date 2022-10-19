import { COLORS } from "constants/colors";
import styled, { keyframes } from "styled-components";

const rotateAnimation = keyframes`
0%{
transform: rotate(0deg) scale(1, 1);
}

50%{
    transform: rotate(180deg) scale(1.5, 1.5);

}

to {
    transform: rotate(360deg) scale(1, 1);
}
`;

export const MainPageStyled = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100vw;
    height: 100vh;
    background-color: ${COLORS.BackgroundDark};
`;

export const ContentStyled = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 1340px;
    padding: 20px 0;

    h1 {
        color: #1b1b1b;
        font-size: 80px;
    }

    h3 {
        color: #525252;
    }
`;

export const TobaccosStyled = styled.div`
    display: flex;
    flex-direction: column;
    width: calc(100% - 420px);
    gap: 16px;
`;

export const TableStyled = styled.div`
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin-top: 60px;
`;

export const BannerStyled = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid ${COLORS.BorderColor};
    border-radius: 200px;
    width: 360px;
    height: 100%;
    max-height: 500px;
    font-style: italic;

    font-size: 40px;
    color: #ff2e51;
    text-align: center;

    background-color: yellow;

    animation: ${rotateAnimation} infinite 6s linear;
`;
