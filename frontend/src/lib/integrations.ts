import type { UploadResponse, Point } from "./types";

export const ConvertImgToBase64 = async (targetImg: HTMLImageElement) => {
	const image = new Image();
	image.crossOrigin = "Anonymous"; // Prevent CORS issues for external images
	image.src = targetImg.src;

	await new Promise((resolve, reject) => {
		image.onload = resolve;
		image.onerror = reject;
	});

	const canvas = document.createElement("canvas");
	canvas.width = image.width;
	canvas.height = image.height;

	const context = canvas.getContext("2d");
	context?.drawImage(image, 0, 0);

	const base64String = canvas.toDataURL("image/png"); // Adjust format if needed
	canvas.remove();
	return base64String.substring(22); // removing the png prefix [rework]
}

export const GetSegments = async (segmentsPromise: Promise<Response>) => {
	let res = await segmentsPromise;

	if (!res.ok) {
		return [];
	}

	let data: any;
	try {
		data = await res.json();
	} catch {
		return [];
	}

	let newPolygons: Point[][] = [];
	for (let k in data["segments"]) {
		if (k == "Type") {
			console.log("Type of car is: ", data["segments"][k]);
			continue;
		}

		let index = newPolygons.push([]) - 1;
		for (let vertex of data["segments"][k]) {
			newPolygons[index].push({
				x: vertex[0],
				y: vertex[1],
			});
		}
	}

	return newPolygons;
};

