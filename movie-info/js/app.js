import 'regenerator-runtime/runtime';
import axios from 'axios';

const movieTitle = document.getElementById('title');
const movieGenre = document.getElementById('genre');
const movieYear = document.getElementById('year')

// Get list of movies
axios.get('/movies')
  .then(response => {
    response.data.forEach(movie => {
      const li = document.createElement('li');
      li.innerHTML = `${movie.title} (${movie.genre}, ${movie.year}) <button class="delete-movie" data-id="${movie.id}">Delete</button>`;
      movieList.appendChild(li);
    });
  })
  .catch(error => {
    console.log(error);
  });

// Add movie
addMovieForm.addEventListener('submit', event => {
  event.preventDefault();
  const title = document.getElementById('title').value;
  const genre = document.getElementById('genre').value;
  const year = document.getElementById('year').value;
  axios.post('/movies', { title, genre, year })
    .then(response => {
      const movie = response.data;
      const li = document.createElement('li');
      li.innerHTML = `${movie.title} (${movi.genre}, ${movie.year}) <button class="delete-movie" data-id="${movie.id}">Delete</button>`;
      movieList.appendChild(li);
      addMovieForm.reset();
    })
    .catch(error => {
      console.log(error);
    });
});

// Delete movie
movieList.addEventListener('click', event => {
  if (event.target.classList.contains('movie_delete')) {
    const id = event.target.dataset.id;
    axios.delete(`/movies/${id}`)
      .then(response => {
        const li = event.target.parentNode;
        li.parentNode.removeChild(li);
      })
      .catch(error => {
        console.log(error);
      });
  }
});

// Edit movie
movieList.addEventListener('click', event => {
  if (event.target.classList.contains('movie_update')) {
    const id = event.target.dataset.id;
    const title = prompt('Enter new title:');
    const genre = prompt('Enter new director:');
    const year = prompt('Enter new year:');
    axios.put(`/movies/${id}`, { title, director, year })
      .then(response => {
        const movie = response.data;
        const li = event.target.parentNode;
        li.innerHTML = `${movie.title} (${movie.director}, ${movie.year}) <button class="delete-movie" data-id="${movie.id}">Delete</button> <button class="edit-movie" data-id="${movie.id}">Edit</button>`;
      })
      .catch(error => {
        console.log(error);
      });
  }
});