import React, {useState,useEffect} from 'react'
import SearchBar from "./Components/SearchBar";
import "./App.css";
import MovieList from './Components/MovieList';
import MovieListHeading from './Components/MovieListHeading';

function App() {
  const [data,setData] = useState([{}])
  const [list, setList] = useState([ { "title": "Aliens", "poster": "https://image.tmdb.org/t/p/w500/r1x5JGpyqZU8PYhbs4UcrO1Xb6x.jpg" }, { "title": "Silent Running", "poster": "https://image.tmdb.org/t/p/w500/uWoj7EfHBprcssXUzCCWeI383Tx.jpg" }, { "title": "Moonraker", "poster": "https://image.tmdb.org/t/p/w500/6LrJdXNmu5uHOVALZxVYd44Lva0.jpg" }, { "title": "Alien", "poster": "https://image.tmdb.org/t/p/w500/vfrQk5IPloGg1v9Rzbh2Eg3VGyM.jpg" }, { "title": "Mission to Mars", "poster": "https://image.tmdb.org/t/p/w500/beDWEWxgFlt1UWvf2al9cjDol2i.jpg" } ])
  const [searched, setSearched] = useState([{}])
  const [mightLike, setMightLike] = useState([{"title": "Aliens", "poster": "https://image.tmdb.org/t/p/w500/r1x5JGpyqZU8PYhbs4UcrO1Xb6x.jpg" }, { "title": "Silent Running", "poster": "https://image.tmdb.org/t/p/w500/uWoj7EfHBprcssXUzCCWeI383Tx.jpg" }, { "title": "Moonraker", "poster": "https://image.tmdb.org/t/p/w500/6LrJdXNmu5uHOVALZxVYd44Lva0.jpg" }, { "title": "Alien", "poster": "https://image.tmdb.org/t/p/w500/vfrQk5IPloGg1v9Rzbh2Eg3VGyM.jpg" }, { "title": "Mission to Mars", "poster": "https://image.tmdb.org/t/p/w500/beDWEWxgFlt1UWvf2al9cjDol2i.jpg"}])
  const [addSearched, setAddSearched] = useState(" ")

  
  useEffect(() => {
    fetch("/titles").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
      }
    )
  },[])


  useEffect(() => {
    fetch("/searched").then(
      res => res.json()
    ).then(
      searched => {
        setSearched(searched)
      }
    )
  },[])

  const handleSearchedChange = (inputValue) =>{
    setAddSearched(inputValue)
  }

  const handleSubmit = () =>{
    fetch("/recommend",{
      method:"POST",
      body: JSON.stringify({
        name: addSearched
      }),
      headers:{
        "Content-type" : "application/json; charset=UTF-8"
      }
    }).then(response => response.json()
      .then(message => {
        console.log(message)
        setAddSearched(" ")
      }).then(ChangeList
        ).then(ChangeMightLike)
    )
  }

  const ChangeList = () =>{
      fetch("/similar").then(
        res => res.json()
      ).then(
        list => {
          setList(list)
        }
      )
  }

  const ChangeMightLike = () =>{
    fetch("/mightLike").then(
      res => res.json()
    ).then(
      mightLike => {
        setMightLike(mightLike)
      }
    )
  }

  

  return (
    <div className='container-fluid movie-app'>
      <MovieListHeading heading='Movie Recommender' />
      
      <div className='row d-flex align-items-center mt-4 mb-4'>
      <div className='row d-flex align-items-center mt-4 mb-4'>
      <label id="fname">Enter a movie you like: </label>
          <SearchBar userInput = {addSearched} onFormChange = {handleSearchedChange} onFormSubmit = {handleSubmit}/>
      </div>
      <div className = "movies-list">
        <lable id="movielist">Scroll down to see all the movies in the database: </lable>
        <div className="dataResult" >
          {data.map((value,key)=>{
          return <div class="dataItem"> {value.title} </div>
          })}
        </div>
      </div>
      </div>
      
    
    <div className='row d-flex align-items-center mt-4 mb-4'>
				<MovieListHeading heading='Similar Movies' />
		</div>
    <div className='row'>
      <MovieList
        movies = {list}
      />
    </div>
    <div className='row d-flex align-items-center mt-4 mb-4'>
				<MovieListHeading heading='Movies You Moight Like' />
		</div>
    <div className='row'>
      <MovieList
        movies = {mightLike}
      />
    </div>
    </div>
  );
} 

export default App;
