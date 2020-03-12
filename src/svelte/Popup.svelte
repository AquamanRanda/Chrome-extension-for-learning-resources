<script> 
export let name;
let cost=false;
import { onMount } from "svelte";
import axios from 'axios'
    const apiURL = "http://127.0.0.1:2000/";
	let data = {programs:[]};
	let datas;
	onMount(async function() {
        const response = await fetch(apiURL);
		data = await response.json();
	});
	async function apicall (name) {
		console.log(name);
		const apiURLs = `http://127.0.0.1:2000/${name}`;
		console.log(apiURLs);
		const responses = await axios.get(apiURLs);
		console.log(responses);
		datas = responses.data.program[name];
		console.log(datas.free_top3);
		for (let x in datas.free_top3){
			console.log(x);
			console.log(datas.free_top3[x])
		}
		cost=true;
	};
</script>

<h1>{name}!</h1>
<h2>Programming Languages</h2>
<img alt="logo" src="/icon128.png">
<div class='program'>
	{#each data.programs as item }
        	<div class="lang">
                <p on:click={apicall(item.name)}> {item.name}</p>
            </div>
    {/each}
</div>
{#if cost}
<div>
	Featured:
	{Object.keys(datas.featured)[0]}  - <a href={Object.values(datas.featured)[0]}>Click here!</a>
	<div>
	Free resourses:
	{#each Object.keys(datas) as item,i}
		<div>
			{Object.keys(datas.free_top3)[i]}  - <a href={Object.values(datas.free_top3)[i]}>Click here!</a>
		</div>
	{/each}
	</div>
	<div>
	Paid resourses:
	{#each Object.keys(datas) as item,i}
		<div>
			{Object.keys(datas.paid_top3)[i]}  - <a href={Object.values(datas.paid_top3)[i]}>Click here!</a>
		</div>
	{/each}
	</div>
</div>
{/if}
<style>
	p{
		cursor: pointer;
	}
	h2{
		color:	red;
		text-align: center
	}
	h1 {
		color: blue;
		text-align: center
	}

</style>