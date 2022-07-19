import React, {useState} from 'react';
import { Col, Row, Spinner} from "react-bootstrap";
import MusicCard from "../../components/MusicCard";
import InputField from "../../components/InputField";
import { getMusicByName } from '../../modules'
import './ITunesPage.css';
import {useWindowSize} from "../../hooks/useWindowSize";

function ITunesPage() {

    const [searchValue, setSearchValue] = useState('radiohead');

    const [filter, setFilter] = useState('');

    const [loading, setLoading] = useState(false)

    const [music, setMusic] = useState([])

    const handleSearch = async () => {
        // Сбрасываем фильтр
        await setFilter('');
        // Ставим загрузку
        await setLoading(true);
        const { results } = await getMusicByName(searchValue);
        // Добавляем в состояние только треки
        await setMusic(results.filter(item => item.wrapperType === "track"));
        // Убираем загрузку
        await setLoading(false)
    }

    const handleFilter = ()=> {
        setMusic(music => music.filter(item=>item.artistName && item.artistName.includes(filter)));
    }

    const { width } = useWindowSize();
    const isMobile = width && width <= 600;

    return (
        <div className={`container ${loading && 'containerLoading'}`}>
            {loading && <div className="loadingBg"><Spinner animation="border"/></div>}
            <InputField value={searchValue} setValue={setSearchValue} placeholder="поиск" loading={loading} onSubmit={handleSearch} buttonTitle="Искать"/>
            <InputField value={filter} setValue={setFilter} placeholder="Автор" loading={loading} onSubmit={handleFilter} buttonTitle="Отфильтровать"/>
            {!music.length ? <h1>К сожалению, пока ничего не найдено :(</h1>:
                <Row xs={1} md={isMobile ? 1 : 4} className="g-4">
                {music.map((item, index)=>{
                    return isMobile ? <MusicCard {...item} key={index}/> :(
                        <Col key={index}>
                            <MusicCard {...item}/>
                        </Col>
                    )
                })}
            </Row>
            }
    </div>
    );
}

export default ITunesPage;
