<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\Facades\Storage;

/**
 * @tags Определение дефекта
 */
class DefectDetectionController extends Controller
{
    /**
     * Загрузка изображения сварки
     *
     * @response array{image: string}
     */
    public function uploadImage(Request $request): JsonResource
    {
        $request->validate([
            'image' => 'required|image|mimes:jpeg,png,jpg|max:4048',
        ]);

        $image = $request->file('image');

        $image->storeAs('images', $image->hashName());

        return new JsonResource([
            'image' => Storage::disk('public')->url('images/' . $image->hashName()),
        ]);
    }
}
