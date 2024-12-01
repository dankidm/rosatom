import type { AABB, Point } from "./types";

// Преобразует набор точек в формат используемый аттрибутом `path` svg элемента
export const PolygonToSVGPath = (polygon: Point[]) => {
	let path = "";

	for (let i = 0; i < polygon.length; i++) {
		path = `${path} ${polygon[i].x},${polygon[i].y}`;
	}

	return path;
};

export const GetAABB = (polygon: Point[]) => {
	let aabb: AABB = {
		min: {
			x: polygon[0].x,
			y: polygon[0].y,
		},
		max: {
			x: polygon[0].x,
			y: polygon[0].y,
		}
	}

	for (let i = 0; i < polygon.length; i++) {
		aabb.min.x = Math.min(polygon[i].x, aabb.min.x);
		aabb.max.x = Math.max(polygon[i].x, aabb.max.x);
		aabb.min.y = Math.min(polygon[i].y, aabb.min.y);
		aabb.max.y = Math.max(polygon[i].y, aabb.max.y);
	}

	return aabb;
}

export const IsPointInAABB = (point: Point, aabb: AABB) => {
	return !(point.x < aabb.min.x
		|| point.x > aabb.max.x
		|| point.y < aabb.min.y
		|| point.y > aabb.max.y);
}

export const IsPointInPolygon = (point: Point, polygon: Point[]) => {
	if (!IsPointInAABB(point, GetAABB(polygon))) {
		return false;
	}

	let isInside = false;

	let i = 0;
	let j = polygon.length - 1;

	while (i < polygon.length) {
		if (polygon[i].y > point.y != polygon[j].y > point.y &&
			point.x <
			((polygon[j].x - polygon[i].x) * (point.y - polygon[i].y)) /
			(polygon[j].y - polygon[i].y) +
			polygon[i].x
		) {
			isInside = !isInside;
		}

		j = i;
		i += 1;
	}

	return isInside;
}

export const TransformPolygon = (polygon: Point[], targetElement: DOMRect, baseSize: number) => {
	let newPoly: Point[] = [];
	let scaleX = targetElement.width / baseSize;
	let scaleY = targetElement.height / baseSize;

	for (let i = 0; i < polygon.length; i++) {
		newPoly.push({
			x: polygon[i].x * scaleX + targetElement.x,
			y: polygon[i].y * scaleY + targetElement.y,
		});
	}

	return newPoly;
}
