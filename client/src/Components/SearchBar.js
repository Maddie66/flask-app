import React from "react";
import "./SearchBar.css";


export const SearchBar = ({ userInput,onFormChange, onFormSubmit}) =>{

  const handleChange = (event) => {
    onFormChange(event.target.value)
  }
  
  const handleSubmit = (event) =>{
    event.preventDefault()
    onFormSubmit()
  }

  const clear_data = () =>{
    fetch("/clear")
      .then(
        console.log("cleared")
      )
  }
  return (
    <>
      <form onSubmit={handleSubmit}>
        <input class="search" type="text" size={"30"} value = {userInput} onChange = {handleChange}></input>
        <input class="button" type='submit' value = "Search"></input>
        <button onClick = {clear_data} >Clear History</button>
      </form>
    </>
  ); 
}

export default SearchBar;
