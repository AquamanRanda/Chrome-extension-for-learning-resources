<script>
  export let name;
  let cost = false;
  import { onMount } from "svelte";
  import axios from "axios";
  const apiURL = "https://apiforlearning.osc-fr1.scalingo.io/";
  let data = { programs: [] };
  let datas;
  onMount(async function() {
    const response = await fetch(apiURL);
    data = await response.json();
  });
  async function apicall(name) {
    console.log(name);
    const apiURLs = `https://apiforlearning.osc-fr1.scalingo.io/${name}`;
    console.log(apiURLs);
    const responses = await axios.get(apiURLs);
    console.log(responses);
    datas = responses.data.program[name];
    console.log(datas.free_top3);
    for (let x in datas.free_top3) {
      console.log(x);
      console.log(datas.free_top3[x]);
    }
    cost = true;
  }
  function openInNewTab(url) {
    var win = window.open(url, "_blank");
    win.focus();
  }
</script>

<style>
  p {
    cursor: pointer;
  }
  h2 {
    color: red;
    text-align: center;
  }
  h1 {
    color: blue;
    text-align: center;
  }
  h6 {
    cursor: pointer;
    text-decoration: underline;
  }
  h4 {
    color: darkgreen;
  }
</style>

<h1>{name}!</h1>
<h2>Programming Languages</h2>
<img alt="logo" src="/icon128.png" />
<h3>Click and scroll down to see the resources!</h3>
<div class="program">
  {#each data.programs as item}
    <div class="lang">
      <p on:click={apicall(item.name)}>{item.name}</p>
    </div>
  {/each}
</div>
{#if cost}
  <div class="container">
    <h4>Featured:</h4>
    <div class="featured">
      {Object.keys(datas.featured)[0]} -
      <h6 on:click={openInNewTab(Object.values(datas.featured)[0])}>
        Click here!
      </h6>
    </div>
    <h4>Free resourses:</h4>
    <div class="free">
      {#each Object.keys(datas) as item, i}
        {Object.keys(datas.free_top3)[i]} -
        <h6 on:click={openInNewTab(Object.values(datas.free_top3)[i])}>
          Click here!
        </h6>
      {/each}
    </div>
    <h4>Paid resourses:</h4>
    <div class="paid">
      {#each Object.keys(datas) as item, i}
        {Object.keys(datas.paid_top3)[i]} -
        <h6 on:click={openInNewTab(Object.values(datas.paid_top3)[i])}>
          Click here!
        </h6>
      {/each}
    </div>
  </div>
{/if}
