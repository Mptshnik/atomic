<?php

namespace App\Services;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;

class DefectDetectionService
{
    public function processImage(Request $request): ?array
    {
        $script = 'defect.py';

        $pythonScriptPath = base_path('python/' . $script);

        $file = $request->file('file');

        $filePath = $file->storeAs('files', $file->hashName());

        $process = new Process([
            'python3',
            $pythonScriptPath,
            storage_path('app/public/' . $filePath),
        ]);

        $process->run();

        if (! $process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }

        $output = explode("\n", $process->getOutput());

        $result = isset($output[1]) ? json_decode($output[1], true) : null;

        if (! $result) {
            return null;
        }

        $result['image'] = config('app.url') . '/' . $result['image'];

        return [
            'output' => $result,
        ];
    }
}
