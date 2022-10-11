import {useEffect, useState} from 'react';

function Joke() {
    const [joke, setJoke] = useState({});

    useEffect(() => {
        fetch('https://official-joke-api.appspot.com/jokes/programming/random')
            .then(response => response.json()[0])
            .then(json => {
                setJoke(json[0]);
            });
        
    }, []);

    const {setup, punchline} = joke;

    return (
        <div>
            <h3>Joke</h3>
            <p>{setup}</p>
            <p><em>{punchline}</em></p>
        </div>
    )
}

export default Joke;