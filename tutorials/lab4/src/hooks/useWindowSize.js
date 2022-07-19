import {useEffect, useState} from "react";

// Пример пользовательского хука (Называйте пользовательские хуки с use в начале!)

export const useWindowSize = () => {
    // в данном пользовательском хуке мы используем хук состояния и хук эффекта
    const [windowSize, setWindowSize] = useState({
        width: undefined,
        height: undefined,
    });
    useEffect(() => {
        // при вызове этой функции, мы будем "класть" в состояние актуальную высоту и ширирну экрана
        function handleResize() {
            setWindowSize({
                width: window.innerWidth,
                height: window.innerHeight,
            });
        }
        // В данном примере мы будет подписываться на изменение размеров экрана, чтобы всегда иметь актуальные данные
        window.addEventListener("resize", handleResize);
        handleResize();
        // После того, как компонент "уничтожается", желательно избавиться от всех "слушателей", чтобы не тратить ресурсы браузера
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    return windowSize;
}
