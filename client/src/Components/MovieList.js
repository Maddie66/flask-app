import React from 'react';

const MovieList = (props) => {
	return (
		<>
			{props.movies.map((value) => (
				<div key={value.id}  className='image-container d-flex justify-content-start m-3'>
					<img key={value.id} src={value.poster} alt='movie'></img>
				</div>
			))}
		</>
	);
};

export default MovieList;
 